#!/usr/bin/env sh
set -eu

cd "$(dirname "$0")"
mkdir -p build

usage() {
    echo "Usage: $0 {python|javascript|java|c|cpp|csharp|go|rust|php|ruby|bash|perl|lua|tcl|awk|asm}" >&2
    exit 2
}

install_package() {
    package=$1

    if command -v apt-get >/dev/null 2>&1; then
        manager=apt-get
    elif command -v dnf >/dev/null 2>&1; then
        manager=dnf
    elif command -v yum >/dev/null 2>&1; then
        manager=yum
    elif command -v pacman >/dev/null 2>&1; then
        manager=pacman
    elif command -v zypper >/dev/null 2>&1; then
        manager=zypper
    elif command -v brew >/dev/null 2>&1; then
        manager=brew
    else
        echo "No supported package manager found. On macOS, install Homebrew first; otherwise install '$package' with your system package manager." >&2
        return 1
    fi

    brew_package=$package
    if [ "$manager" = brew ]; then
        case "$package" in
            python3) brew_package=python ;;
            nodejs) brew_package=node ;;
            default-jdk) brew_package=openjdk ;;
            build-essential) brew_package=gcc ;;
            mono-mcs|mono-runtime) brew_package=mono ;;
            golang-go) brew_package=go ;;
            php-cli) brew_package=php ;;
            rustc) brew_package=rust ;;
            lua5.4) brew_package=lua ;;
            tcl) brew_package=tcl-tk ;;
            mawk) brew_package=awk ;;
        esac
    fi

    echo "This will install '$brew_package' using $manager."
    printf "Download and install '$brew_package'? [y/N] "
    if [ ! -r /dev/tty ]; then
        echo "Cannot ask for confirmation because this terminal has no interactive input." >&2
        return 1
    fi
    IFS= read -r answer </dev/tty
    case "$answer" in
        y|Y|yes|YES|Yes) ;;
        *) echo "Installation cancelled." >&2; return 1 ;;
    esac

    if [ "$manager" = brew ]; then
        brew install "$brew_package"
        return $?
    fi

    if [ "$(id -u)" -ne 0 ] && ! command -v sudo >/dev/null 2>&1; then
        echo "Installation needs root access, but sudo was not found." >&2
        return 1
    fi

    case "$manager" in
        apt-get) set -- apt-get install -y "$package" ;;
        dnf)     set -- dnf install -y "$package" ;;
        yum)     set -- yum install -y "$package" ;;
        pacman)  set -- pacman -S --noconfirm "$package" ;;
        zypper)  set -- zypper --non-interactive install "$package" ;;
    esac

    if [ "$(id -u)" -eq 0 ]; then
        "$@"
    else
        sudo "$@"
    fi
}

require_tool() {
    tool=$1
    package=$2
    if ! command -v "$tool" >/dev/null 2>&1; then
        echo "Required command '$tool' is missing." >&2
        install_package "$package" || exit 1
        if ! command -v "$tool" >/dev/null 2>&1; then
            echo "Installation finished, but '$tool' is still unavailable." >&2
            exit 1
        fi
    fi
}

require_apple_command_line_tools() {
    tool=$1
    if command -v "$tool" >/dev/null 2>&1; then
        return
    fi

    echo "Required command '$tool' is missing. macOS provides it with Xcode Command Line Tools."
    printf "Start the Command Line Tools installer now? [y/N] "
    if [ ! -r /dev/tty ]; then
        echo "Cannot ask for confirmation because this terminal has no interactive input." >&2
        exit 1
    fi
    IFS= read -r answer </dev/tty
    case "$answer" in
        y|Y|yes|YES|Yes)
            xcode-select --install
            echo "Complete the Apple installer, then run this command again."
            exit 1
            ;;
        *) echo "Installation cancelled." >&2; exit 1 ;;
    esac
}

[ "$#" -eq 1 ] || usage

case "$1" in
    python)
        require_tool python3 python3
        exec python3 hello_world.py
        ;;
    javascript)
        require_tool node nodejs
        exec node hello_world.js
        ;;
    java)
        require_tool javac default-jdk
        javac -d build HelloWorld.java
        exec java -cp build HelloWorld
        ;;
    c)
        if [ "$(uname -s)" = Darwin ]; then
            require_apple_command_line_tools cc
        else
            require_tool cc build-essential
        fi
        cc hello_world.c -o build/hello_world_c
        exec build/hello_world_c
        ;;
    cpp)
        if [ "$(uname -s)" = Darwin ]; then
            require_apple_command_line_tools c++
        else
            require_tool c++ build-essential
        fi
        c++ hello_world.cpp -o build/hello_world_cpp
        exec build/hello_world_cpp
        ;;
    csharp)
        if ! command -v mcs >/dev/null 2>&1; then
            require_tool mcs mono-mcs
        fi
        require_tool mono mono-runtime
        mcs -out:build/HelloWorld.exe HelloWorld.cs
        exec mono build/HelloWorld.exe
        ;;
    go)
        require_tool go golang-go
        exec go run hello_world.go
        ;;
    rust)
        require_tool rustc rustc
        rustc hello_world.rs -o build/hello_world_rust
        exec build/hello_world_rust
        ;;
    php)
        require_tool php php-cli
        exec php hello_world.php
        ;;
    ruby)
        require_tool ruby ruby
        exec ruby hello_world.rb
        ;;
    bash)
        require_tool bash bash
        exec bash hello_world.sh
        ;;
    perl)
        require_tool perl perl
        exec perl hello_world.pl
        ;;
    lua)
        require_tool lua lua5.4
        exec lua hello_world.lua
        ;;
    tcl)
        require_tool tclsh tcl
        exec tclsh hello_world.tcl
        ;;
    awk)
        require_tool awk mawk
        exec awk -f hello_world.awk
        ;;
    asm)
        require_tool nasm nasm
        if [ "$(uname -s)" = Darwin ]; then
            require_apple_command_line_tools clang
            nasm -f macho64 hello_world_macos.asm -o build/hello_world_macos.o
            clang -arch x86_64 build/hello_world_macos.o -o build/hello_world_macos
            if [ "$(uname -m)" = arm64 ]; then
                if ! arch -x86_64 /usr/bin/true >/dev/null 2>&1; then
                    echo "This NASM program is x86-64 and needs Rosetta 2 to run on Apple Silicon."
                    printf "Download and install Rosetta 2 now? [y/N] "
                    if [ ! -r /dev/tty ]; then
                        echo "Cannot ask for confirmation because this terminal has no interactive input." >&2
                        exit 1
                    fi
                    IFS= read -r answer </dev/tty
                    case "$answer" in
                        y|Y|yes|YES|Yes)
                            softwareupdate --install-rosetta --agree-to-license
                            ;;
                        *) echo "Installation cancelled." >&2; exit 1 ;;
                    esac
                fi
                exec arch -x86_64 build/hello_world_macos
            fi
            exec build/hello_world_macos
        else
            require_tool ld binutils
            nasm -f elf64 hello_world.asm -o build/hello_world.o
            ld build/hello_world.o -o build/hello_world_asm
            exec build/hello_world_asm
        fi
        ;;
    *) usage ;;
esac
