#!/usr/bin/env sh
set -eu

cd "$(dirname "$0")"
mkdir -p build

usage() {
    echo "Usage: $0 {python|javascript|java|c|cpp|csharp|go|rust|php|ruby|asm}" >&2
    exit 2
}

[ "$#" -eq 1 ] || usage

case "$1" in
    python)    exec python3 hello_world.py ;;
    javascript) exec node hello_world.js ;;
    java)
        javac -d build HelloWorld.java
        exec java -cp build HelloWorld
        ;;
    c)
        cc hello_world.c -o build/hello_world_c
        exec build/hello_world_c
        ;;
    cpp)
        c++ hello_world.cpp -o build/hello_world_cpp
        exec build/hello_world_cpp
        ;;
    csharp)
        if command -v mcs >/dev/null 2>&1; then
            mcs -out:build/HelloWorld.exe HelloWorld.cs
            if command -v mono >/dev/null 2>&1; then
                exec mono build/HelloWorld.exe
            fi
            exec build/HelloWorld.exe
        elif command -v csc >/dev/null 2>&1; then
            csc -out:build/HelloWorld.exe HelloWorld.cs
            if command -v mono >/dev/null 2>&1; then
                exec mono build/HelloWorld.exe
            fi
            exec build/HelloWorld.exe
        else
            echo "Install Mono (mcs or csc) or use the .NET SDK; see README.md." >&2
            exit 1
        fi
        ;;
    go)        exec go run hello_world.go ;;
    rust)
        rustc hello_world.rs -o build/hello_world_rust
        exec build/hello_world_rust
        ;;
    php)       exec php hello_world.php ;;
    ruby)      exec ruby hello_world.rb ;;
    asm)
        nasm -f elf64 hello_world.asm -o build/hello_world.o
        ld build/hello_world.o -o build/hello_world_asm
        exec build/hello_world_asm
        ;;
    *) usage ;;
esac
