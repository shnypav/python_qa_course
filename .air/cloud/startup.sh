#!/usr/bin/env bash
# Air runs this after checkout and on every resume. Keep successful setup cached.
set -Eeuo pipefail
umask 022

trap 'printf "[air-startup] Setup failed at line %s; see the error above.\n" "$LINENO" >&2' ERR

REPO_ROOT=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)
STATE_DIR=${AIR_QA_STATE_DIR:-${XDG_DATA_HOME:-$HOME/.local/share}/air/python-qa-course}
MAIN_VENV="$STATE_DIR/venv"
SELENIUM_VENV="$STATE_DIR/selenium-venv"
BROWSERS_DIR="$STATE_DIR/browsers"
QA_DISPLAY=${AIR_QA_DISPLAY:-:99}
ECHO_PORT=${AIR_QA_ECHO_PORT:-8080}

log() { printf '[air-startup] %s\n' "$*"; }
fail() { log "$*" >&2; exit 1; }
download() {
    curl --fail --location --silent --show-error --retry 2 \
        --connect-timeout 15 --max-time 300 "$1" --output "$2"
}

[[ $(uname -s) == Linux && $(uname -m) == x86_64 ]] ||
    fail 'Use a Linux x86-64 cloud environment: the NASM tests build x86-64 ELF binaries.'
command -v apt-get >/dev/null || fail 'This startup script requires an Ubuntu/Debian cloud image.'
[[ $STATE_DIR == /* ]] || fail 'AIR_QA_STATE_DIR must be an absolute path.'
[[ $QA_DISPLAY =~ ^:[0-9]+$ ]] || fail 'AIR_QA_DISPLAY must be a local display such as :99.'
[[ $ECHO_PORT =~ ^[0-9]+$ && $ECHO_PORT -gt 0 && $ECHO_PORT -le 65535 ]] ||
    fail 'AIR_QA_ECHO_PORT must be between 1 and 65535.'

sudo_cmd=()
if (( EUID != 0 )); then
    command -v sudo >/dev/null || fail 'The environment user needs sudo rights.'
    sudo_cmd=(sudo -n)
fi

mkdir -p "$STATE_DIR/bin" "$STATE_DIR/logs" "$BROWSERS_DIR"
WORK_DIR=$(mktemp -d "$STATE_DIR/setup.XXXXXX")
trap 'rm -rf -- "$WORK_DIR"' EXIT

# Shell, language runtimes, build tools, process utilities, and browser libraries.
packages=(
    ca-certificates curl git unzip xz-utils bzip2 fish passwd diffutils
    python3 python3-dev python3-pip python3-venv
    build-essential binutils nasm nodejs default-jdk-headless
    mono-mcs mono-runtime golang-go rustc php-cli ruby
    procps iproute2 net-tools lsof util-linux
    xvfb xauth x11-utils fonts-liberation fonts-dejavu-core
    libnss3 libnspr4 libgbm1 libx11-xcb1 libxss1 libdbus-glib-1-2
)
compat_libraries=(libgtk-3-0 libasound2 libxt6)
package_hash=$(printf '%s\n' "${packages[@]}" "${compat_libraries[@]}" | sha256sum | cut -d ' ' -f 1)
packages_ready=false
if [[ -r "$STATE_DIR/packages.sha256" && -r "$STATE_DIR/packages.txt" ]] &&
    [[ $(cat "$STATE_DIR/packages.sha256") == "$package_hash" ]]; then
    packages_ready=true
    while IFS= read -r package; do
        if [[ $(dpkg-query -W -f='${Status}' "$package" 2>/dev/null) != 'install ok installed' ]]; then
            packages_ready=false
            break
        fi
    done < "$STATE_DIR/packages.txt"
fi

if [[ $packages_ready == false ]]; then
    log 'Installing language toolchains, browser libraries, and OS utilities.'
    "${sudo_cmd[@]}" env DEBIAN_FRONTEND=noninteractive apt-get update
    # Ubuntu 24.04/Debian 13 renamed these packages for the time_t transition.
    for package in "${compat_libraries[@]}"; do
        if apt-cache show "${package}t64" >/dev/null 2>&1; then
            packages+=("${package}t64")
        else
            packages+=("$package")
        fi
    done
    "${sudo_cmd[@]}" env DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends "${packages[@]}"
    printf '%s\n' "${packages[@]}" > "$STATE_DIR/packages.txt"
    printf '%s\n' "$package_hash" > "$STATE_DIR/packages.sha256"
else
    log 'System packages are already installed.'
fi

# Reproduce the current Fish/Fisher/Pure setup before Python/browser downloads.
FISH_BIN=$(command -v fish)
FISH_CONFIG_DIR=${XDG_CONFIG_HOME:-$HOME/.config}/fish
FISH_PLUGINS_DIR=${XDG_DATA_HOME:-$HOME/.local/share}/fish/plugins

install_fish_plugin() {
    local name=$1 repository=$2 revision=$3 directory
    directory="$FISH_PLUGINS_DIR/$name"
    if [[ $(git -C "$directory" rev-parse --verify HEAD 2>/dev/null || true) != "$revision" ]]; then
        log "Downloading the pinned $name plugin."
        mkdir -p "$directory"
        git -C "$directory" init --quiet
        git -C "$directory" fetch --depth 1 "https://github.com/$repository.git" "$revision"
        git -C "$directory" -c advice.detachedHead=false checkout --detach FETCH_HEAD
    fi

    # Local plugin sources let Fisher reuse downloads and avoid API tarball requests.
    # shellcheck disable=SC2016
    "$FISH_BIN" -c '
        source $argv[1]/functions/fisher.fish
        functions --query fisher; or exit 1
        set --local fisher_path $__fish_config_dir
        set --local plugin $argv[2]
        set --local files $plugin/{functions,conf.d,completions,themes}/*
        set --local needs_install false
        for file in $files
            set --local target (string replace -- "$plugin/" "$fisher_path/" "$file")
            if not command cmp --silent -- "$file" "$target"
                set needs_install true
            end
        end
        if not contains -- "$plugin" $_fisher_plugins
            set needs_install true
            # Preserve an unmanaged prompt before Fisher replaces its files.
            set --local backup_dir
            for file in $files
                set --local relative (string replace -- "$plugin/" "" "$file")
                set --local target "$fisher_path/$relative"
                if test -e "$target"; or test -L "$target"
                    if not set --query backup_dir[1]
                        command mkdir -p "$fisher_path/backups"; or exit 1
                        set backup_dir (command mktemp -d "$fisher_path/backups/air-startup.XXXXXX"); or exit 1
                    end
                    command mkdir -p "$backup_dir/"(command dirname -- "$relative"); or exit 1
                    command mv -- "$target" "$backup_dir/$relative"; or exit 1
                end
            end
        end
        if test "$needs_install" = true
            fisher install "$plugin"; or exit 1
            contains -- "$plugin" $_fisher_plugins; or exit 1
            for file in $files
                set --local target (string replace -- "$plugin/" "$fisher_path/" "$file")
                command cmp --silent -- "$file" "$target"; or exit 1
            end
        end
    ' "$FISH_PLUGINS_DIR/fisher" "$directory" < /dev/null
}

# Pin the revisions currently used here: Fisher 4.4.8 and Pure 4.19.2.
install_fish_plugin fisher jorgebucaran/fisher 791da644d33d392216f6b1a9b5fc1e470db6d7f2
install_fish_plugin pure pure-fish/pure 39ef70d91421322d1f90828d1838f19891f7772c

python3 - "$FISH_BIN" "$FISH_CONFIG_DIR" "$HOME/.bashrc" <<'PY'
from pathlib import Path
import shlex
import sys

fish_bin = shlex.quote(sys.argv[1])
fish_config = Path(sys.argv[2])
bashrc = Path(sys.argv[3])
handoff = f'''if [[ $- == *i* && -t 0 && -t 1 && -z "${{WORKSPACE_FISH_HANDOFF:-}}" && -x {fish_bin} ]]; then
    export WORKSPACE_FISH_HANDOFF=1
    export SHELL={fish_bin}
    exec {fish_bin}
fi'''
content = bashrc.read_text() if bashrc.exists() else ''
if handoff not in content:
    bashrc.write_text(content + '\n# Start Fish in interactive Air terminals; keep nested Bash available.\n' + handoff + '\n')

prompt_config = fish_config / 'conf.d/air-fish-prompt.fish'
prompt_config.parent.mkdir(parents=True, exist_ok=True)
prompt_config.write_text('''# Generated by the Python QA course Air startup script.
set --global pure_enable_git true
set --global pure_show_numbered_git_indicator true
set --global pure_check_for_new_release false
''')
PY

if ! grep -qxF "$FISH_BIN" /etc/shells; then
    printf '%s\n' "$FISH_BIN" | "${sudo_cmd[@]}" tee -a /etc/shells >/dev/null
fi
if [[ $(getent passwd "$(id -un)" | cut -d: -f7) != "$FISH_BIN" ]]; then
    log 'Making Fish the default login shell.'
    "${sudo_cmd[@]}" chsh -s "$FISH_BIN" "$(id -un)"
fi
log 'Fish and the Pure prompt are ready; new interactive terminals will use Fish.'

if [[ ! -x "$MAIN_VENV/bin/python" ]]; then
    python3 -m venv "$MAIN_VENV"
fi

# pytest 6.2.5 and the other Selenium pins belong in their own Python 3.10 env.
# uv downloads a managed interpreter; it does not replace the OS Python.
if [[ ! -x "$SELENIUM_VENV/bin/python" ]]; then
    if command -v python3.10 >/dev/null; then
        python3.10 -m venv "$SELENIUM_VENV"
    else
        if [[ ! -x "$STATE_DIR/bin/uv" ]]; then
            log 'Installing uv to provision the legacy Selenium Python version.'
            download 'https://api.github.com/repos/astral-sh/uv/releases/latest' "$WORK_DIR/uv.json"
            uv_url=$(python3 - "$WORK_DIR/uv.json" <<'PY'
import json
import sys
with open(sys.argv[1]) as source:
    release = json.load(source)
print(next(asset['browser_download_url'] for asset in release['assets']
           if asset['name'] == 'uv-x86_64-unknown-linux-gnu.tar.gz'))
PY
            )
            uv_archive=uv-x86_64-unknown-linux-gnu.tar.gz
            download "$uv_url" "$WORK_DIR/$uv_archive"
            download "$uv_url.sha256" "$WORK_DIR/$uv_archive.sha256"
            (cd "$WORK_DIR" && sha256sum --check "$uv_archive.sha256")
            tar -xzf "$WORK_DIR/$uv_archive" -C "$WORK_DIR"
            install -m 755 "$WORK_DIR/uv-x86_64-unknown-linux-gnu/uv" "$STATE_DIR/bin/uv"
        fi
        UV_PYTHON_INSTALL_DIR="$STATE_DIR/python" "$STATE_DIR/bin/uv" venv \
            --python 3.10 "$SELENIUM_VENV"
    fi
fi

# Use Python's bundled wheels, including after an interrupted venv creation.
for venv in "$MAIN_VENV" "$SELENIUM_VENV"; do
    if ! "$venv/bin/python" -m pip --version >/dev/null 2>&1; then
        "$venv/bin/python" -m ensurepip --upgrade
    fi
done

install_requirements() {
    local venv=$1 requirements=$2 expected
    expected=$( { "$venv/bin/python" --version; sha256sum "$requirements"; } | sha256sum | cut -d ' ' -f 1)
    if [[ -r "$venv/requirements.sha256" ]] &&
        [[ $(cat "$venv/requirements.sha256") == "$expected" ]] &&
        "$venv/bin/python" -m pip check >/dev/null &&
        "$venv/bin/python" -m pip install --disable-pip-version-check --dry-run \
            --no-index -r "$requirements" >/dev/null 2>&1; then
        log "Python dependencies are already installed: $requirements"
        return
    fi
    log "Installing Python dependencies: $requirements"
    "$venv/bin/python" -m pip install --disable-pip-version-check --no-input \
        --timeout 30 --retries 2 -r "$requirements"
    "$venv/bin/python" -m pip check
    printf '%s\n' "$expected" > "$venv/requirements.sha256"
}

install_requirements "$MAIN_VENV" "$REPO_ROOT/requirements.txt"
install_requirements "$SELENIUM_VENV" "$REPO_ROOT/hw_05_06_07_selenium/requirements.txt"

# Download Chrome and ChromeDriver from the SAME official stable release.
# The old webdriver-manager pin cannot discover current Chrome releases.
if [[ ! -x "$BROWSERS_DIR/chrome/chrome" || ! -x "$BROWSERS_DIR/chrome/chromedriver" ]]; then
    log 'Installing a matching Chrome for Testing browser and driver.'
    download 'https://raw.githubusercontent.com/GoogleChromeLabs/chrome-for-testing/gh-pages/last-known-good-versions-with-downloads.json' "$WORK_DIR/chrome.json"
    python3 - "$WORK_DIR/chrome.json" > "$WORK_DIR/chrome-urls.txt" <<'PY'
import json
import sys
with open(sys.argv[1]) as source:
    stable = json.load(source)['channels']['Stable']
for kind in ('chrome', 'chromedriver'):
    print(next(item['url'] for item in stable['downloads'][kind] if item['platform'] == 'linux64'))
PY
    mapfile -t chrome_urls < "$WORK_DIR/chrome-urls.txt"
    download "${chrome_urls[0]}" "$WORK_DIR/chrome.zip"
    download "${chrome_urls[1]}" "$WORK_DIR/chromedriver.zip"
    unzip -q "$WORK_DIR/chrome.zip" -d "$WORK_DIR"
    unzip -q "$WORK_DIR/chromedriver.zip" -d "$WORK_DIR"
    cp -a "$WORK_DIR/chrome-linux64/." "$BROWSERS_DIR/chrome/"
    install -m 755 "$WORK_DIR/chromedriver-linux64/chromedriver" "$BROWSERS_DIR/chrome/chromedriver"
fi

if [[ ! -x "$BROWSERS_DIR/firefox/firefox" || ! -f "$BROWSERS_DIR/firefox/.air-ready" ]]; then
    log 'Installing Firefox without Snap.'
    download 'https://download.mozilla.org/?product=firefox-latest-ssl&os=linux64&lang=en-US' "$WORK_DIR/firefox.tar"
    tar -xf "$WORK_DIR/firefox.tar" -C "$WORK_DIR"
    mkdir -p "$BROWSERS_DIR/firefox"
    cp -a "$WORK_DIR/firefox/." "$BROWSERS_DIR/firefox/"
    touch "$BROWSERS_DIR/firefox/.air-ready"
fi

if [[ ! -x "$STATE_DIR/bin/geckodriver" ]]; then
    log 'Installing GeckoDriver for Firefox.'
    download 'https://api.github.com/repos/mozilla/geckodriver/releases/latest' "$WORK_DIR/geckodriver.json"
    gecko_url=$(python3 - "$WORK_DIR/geckodriver.json" <<'PY'
import json
import sys
with open(sys.argv[1]) as source:
    release = json.load(source)
print(next(asset['browser_download_url'] for asset in release['assets']
           if asset['name'].endswith('-linux64.tar.gz')))
PY
    )
    download "$gecko_url" "$WORK_DIR/geckodriver.tar.gz"
    tar -xzf "$WORK_DIR/geckodriver.tar.gz" -C "$WORK_DIR" geckodriver
    install -m 755 "$WORK_DIR/geckodriver" "$STATE_DIR/bin/geckodriver"
fi

ln -sfn "$BROWSERS_DIR/chrome/chrome" "$STATE_DIR/bin/google-chrome"
ln -sfn "$BROWSERS_DIR/chrome/chromedriver" "$STATE_DIR/bin/chromedriver"
ln -sfn "$BROWSERS_DIR/firefox/firefox" "$STATE_DIR/bin/firefox"

# Startup runs in a separate process: persist the environment for Bash and Fish.
# Prepend the Bash source line so it precedes .bashrc's noninteractive early return
# and the user's interactive handoff to Fish.
python3 - "$STATE_DIR" "$REPO_ROOT" "$QA_DISPLAY" "$ECHO_PORT" "$FISH_CONFIG_DIR" <<'PY'
from pathlib import Path
import shlex
import sys

state, repo = map(Path, sys.argv[1:3])
variables = {
    'AIR_QA_STATE_DIR': str(state),
    'AIR_QA_PYTHON': str(state / 'venv/bin/python'),
    'AIR_QA_SELENIUM_PYTHON': str(state / 'selenium-venv/bin/python'),
    'VIRTUAL_ENV': str(state / 'venv'),
    'CHROME_BIN': str(state / 'browsers/chrome/chrome'),
    'CHROMEDRIVER_PATH': str(state / 'browsers/chrome/chromedriver'),
    'FIREFOX_BIN': str(state / 'browsers/firefox/firefox'),
    'GECKODRIVER_PATH': str(state / 'bin/geckodriver'),
    'AIR_QA_CONTAINER_BROWSER': '1',
    'DISPLAY': sys.argv[3],
    'AIR_QA_ECHO_PORT': sys.argv[4],
}
paths = [str(state / 'venv/bin'), str(state / 'bin')]
shell = ['# Generated by the Python QA course Air startup script.']
shell.extend(f'export {key}={shlex.quote(value)}' for key, value in variables.items())
for path in reversed(paths):
    shell.append(f'case ":$PATH:" in *:{shlex.quote(path)}:*) ;; *) export PATH={shlex.quote(path)}:"$PATH" ;; esac')
shell.extend([
    'for air_qa_host in localhost 127.0.0.1 ::1; do',
    '  case ",${NO_PROXY:-}," in *,$air_qa_host,*) ;; *) export NO_PROXY="${NO_PROXY:+$NO_PROXY,}$air_qa_host" ;; esac',
    'done',
    'export no_proxy="$NO_PROXY"',
    'unset air_qa_host',
])
env_file = state / 'env.sh'
env_file.write_text('\n'.join(shell) + '\n')
source_line = f'[ ! -r {shlex.quote(str(env_file))} ] || . {shlex.quote(str(env_file))}'
for name in ('.bashrc', '.profile'):
    profile = Path.home() / name
    content = profile.read_text() if profile.exists() else ''
    if source_line not in content.splitlines():
        profile.write_text(source_line + '\n' + content)

def fish_quote(value):
    return "'" + value.replace('\\', '\\\\').replace("'", "\\'") + "'"

fish = ['# Generated by the Python QA course Air startup script.']
fish.extend(f'set -gx {key} {fish_quote(value)}' for key, value in variables.items())
for path in reversed(paths):
    fish.append(f'fish_add_path --global --path --prepend {fish_quote(path)}')
fish.extend([
    'for air_qa_host in localhost 127.0.0.1 ::1',
    '    if not contains -- $air_qa_host (string split , -- "$NO_PROXY")',
    '        set -gx NO_PROXY (string join , -- $NO_PROXY $air_qa_host)',
    '    end',
    'end',
    'set -gx no_proxy "$NO_PROXY"',
])
fish_config = Path(sys.argv[5]) / 'conf.d/air-qa-env.fish'
fish_config.parent.mkdir(parents=True, exist_ok=True)
fish_config.write_text('\n'.join(fish) + '\n')
PY
# shellcheck source=/dev/null
source "$STATE_DIR/env.sh"

wait_for() {
    local description=$1
    shift
    for (( attempt=0; attempt<30; attempt++ )); do
        if "$@"; then return; fi
        sleep 1
    done
    fail "$description did not become ready. Check $STATE_DIR/logs."
}

display_ready() { timeout 2 xdpyinfo -display "$DISPLAY" >/dev/null 2>&1; }
if ! display_ready; then
    log "Starting Xvfb on $DISPLAY for the existing graphical browser fixtures."
    nohup setsid Xvfb "$DISPLAY" -screen 0 1920x1080x24 -nolisten tcp -ac \
        > "$STATE_DIR/logs/xvfb.log" 2>&1 < /dev/null &
    wait_for Xvfb display_ready
fi

echo_ready() {
    curl --noproxy '*' --fail --silent --max-time 2 "http://127.0.0.1:$ECHO_PORT/" |
        grep -q 'Response Status: 200 OK'
}
if ! echo_ready; then
    # Refuse to take over a port belonging to another service.
    "$MAIN_VENV/bin/python" - "$ECHO_PORT" <<'PY'
import socket
import sys
with socket.socket() as sock:
    try:
        sock.bind(('127.0.0.1', int(sys.argv[1])))
    except OSError as error:
        raise SystemExit(f'Echo port is unavailable: {error}. Set AIR_QA_ECHO_PORT to a free port.')
PY
    log "Starting the homework echo server on port $ECHO_PORT."
    nohup setsid "$MAIN_VENV/bin/python" -u "$REPO_ROOT/hw_10_echo_server/server.py" --port "$ECHO_PORT" \
        > "$STATE_DIR/logs/echo-server.log" 2>&1 < /dev/null &
    wait_for 'Echo server' echo_ready
fi

log 'Setup complete. New Bash/Fish sessions will use the prepared Python environment.'
log "Run: bash $REPO_ROOT/.air/cloud/run-tests.sh"
