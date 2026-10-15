# Hello World programs

Each program asks for your name and prints a greeting. Run commands from this directory. Install the relevant language runtime or compiler first; the C, C++, Java, C#, Rust, and NASM examples need build tools.

## Run an individual program

```sh
python3 hello_world.py
node hello_world.js
javac HelloWorld.java && java HelloWorld
cc hello_world.c -o build/hello_world_c && ./build/hello_world_c
c++ hello_world.cpp -o build/hello_world_cpp && ./build/hello_world_cpp
csc HelloWorld.cs -out:build/HelloWorld.exe && mono build/HelloWorld.exe
go run hello_world.go
rustc hello_world.rs -o build/hello_world_rust && ./build/hello_world_rust
php hello_world.php
ruby hello_world.rb
nasm -f elf64 hello_world.asm -o build/hello_world.o && ld build/hello_world.o -o build/hello_world_asm && ./build/hello_world_asm
```

Create the build directory before using a command that writes into it:

```sh
mkdir -p build
```

The C# command above uses the Mono compiler (`mcs` is another common compiler name). With the .NET SDK installed, use this instead:

```sh
dotnet new console --output build/csharp --force
cp HelloWorld.cs build/csharp/Program.cs
dotnet run --project build/csharp
```

## Use the launcher

The launcher builds and runs one program. Pass one of: `python`, `javascript`, `java`, `c`, `cpp`, `csharp`, `go`, `rust`, `php`, `ruby`, or `asm`. If its required command is missing, it asks before installing the needed package. It supports Homebrew on macOS, plus apt, dnf, yum, pacman, and zypper on Linux. Linux package installation may ask for your system password through `sudo`.

The assembler launcher selects the Linux ELF example on Linux and the macOS Mach-O example on macOS. The macOS NASM example targets x86-64. On Apple Silicon, the launcher builds it for x86-64 and asks to install Rosetta 2 if needed to run it. NASM and Xcode Command Line Tools (which provide `clang`) are needed on macOS. The launcher can install NASM through Homebrew; install the Command Line Tools with `xcode-select --install` if `clang` is missing.

```sh
./run.sh python
./run.sh asm
```
