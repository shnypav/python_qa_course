#!/usr/bin/env bash
# Independent homeworks register conflicting pytest options; run them separately.
set -Eeuo pipefail

REPO_ROOT=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)
STATE_DIR=${AIR_QA_STATE_DIR:-${XDG_DATA_HOME:-$HOME/.local/share}/air/python-qa-course}
if [[ ! -r "$STATE_DIR/env.sh" ]]; then
    printf 'Run .air/cloud/startup.sh before running the cloud test suites.\n' >&2
    exit 1
fi
# shellcheck source=/dev/null
source "$STATE_DIR/env.sh"

selection=all
if (( $# > 0 )) && [[ $1 != -* ]]; then
    selection=$1
    shift
fi
case "$selection" in
    all) suites=(figures api selenium processes echo hello) ;;
    figures|api|selenium|processes|echo|hello) suites=("$selection") ;;
    *)
        printf 'Usage: %s [all|figures|api|selenium|processes|echo|hello] [pytest arguments...]\n' "$0" >&2
        exit 2
        ;;
esac

run_suite() (
    local suite=$1 directory python=$AIR_QA_PYTHON
    local -a targets options=()
    shift
    case "$suite" in
        figures) directory=hw_02_figures; targets=(tests) ;;
        api) directory=hw_04_api_testing; targets=(.) ;;
        selenium)
            directory=hw_05_06_07_selenium
            python=$AIR_QA_SELENIUM_PYTHON
            targets=(tests)
            ;;
        processes)
            directory=hw_08_ps_aux
            targets=(.)
            options=(--import-mode=importlib)
            ;;
        echo)
            directory=hw_10_echo_server
            targets=(tests)
            options=("--port=$AIR_QA_ECHO_PORT")
            ;;
        hello) directory=hw_11_hello_worlds; targets=(tests) ;;
    esac
    cd -- "$REPO_ROOT/$directory" || return
    export PYTHONPATH="$REPO_ROOT:$PWD${PYTHONPATH:+:$PYTHONPATH}"
    "$python" -m pytest --rootdir="$PWD" --confcutdir="$PWD" \
        "${targets[@]}" "${options[@]}" "$@"
)

result=0
for suite in "${suites[@]}"; do
    printf '\nRunning %s tests\n' "$suite"
    if run_suite "$suite" "$@"; then
        printf '%s: passed\n' "$suite"
    else
        exit_code=$?
        printf '%s: pytest exited with status %s\n' "$suite" "$exit_code" >&2
        result=1
    fi
done
exit "$result"
