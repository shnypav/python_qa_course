#!/usr/bin/env sh
set -eu

cd "$(dirname "$0")"
mkdir -p build

usage() {
    echo "Usage: $0 {python|javascript|java|c|cpp|csharp|go|rust|php|ruby|asm}" >&2
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
    else
        echo "No supported package manager found. Install '$package' manually." >&2
        return 1
    fi

    echo "This will install '$package' using $manager."
    printf "Download and install '$package'? [y/N] "
    if [ ! -r /dev/tty ]; then
        echo "Cannot ask for confirmation because this terminal has no interactive input." >&2
        return 1
    fi
    IFS= read -r answer </dev/tty
    case "$answer" in
        y|Y|yes|YES|Yes) ;;
        *) echo "Installation cancelled." >&2; return 1 ;;
    esac

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
        require_tool cc build-essential
        cc hello_world.c -o build/hello_world_c
        exec build/hello_world_c
        ;;
    cpp)
        require_tool c++ build-essential
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
    asm)
        require_tool nasm nasm
        require_tool ld binutils
        nasm -f elf64 hello_world.asm -o build/hello_world.o
        ld build/hello_world.o -o build/hello_world_asm
        exec build/hello_world_asm
        ;;
    *) usage ;;
esac
