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
bash hello_world.sh
perl hello_world.pl
lua hello_world.lua
tclsh hello_world.tcl
awk -f hello_world.awk
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

The launcher builds and runs one program. Pass one of: `python`, `javascript`, `java`, `c`, `cpp`, `csharp`, `go`, `rust`, `php`, `ruby`, `bash`, `perl`, `lua`, `tcl`, `awk`, or `asm`. If its required command is missing, it asks before installing the needed package. It supports Homebrew on macOS, plus apt, dnf, yum, pacman, and zypper on Linux. Linux package installation may ask for your system password through `sudo`. Lua package names may vary by Linux distribution; install a runtime providing `lua` manually if your package manager does not provide `lua5.4`.

The assembler launcher selects the Linux ELF example on Linux and the macOS Mach-O example on macOS. The macOS NASM example targets x86-64. On Apple Silicon, the launcher builds it for x86-64 and asks to install Rosetta 2 if needed to run it. NASM and Xcode Command Line Tools (which provide `clang`) are needed on macOS. The launcher can install NASM through Homebrew; install the Command Line Tools with `xcode-select --install` if `clang` is missing.

```sh
./run.sh python
./run.sh asm
```

## Run the pytest checks

Install the project dependencies with `python3 -m pip install -r ../requirements.txt`, then run the examples' integration checks from this directory:

```sh
python3 -m pytest -q tests
```

The checks run all sixteen language examples directly and through the launcher, so their matching runtimes and compilers must be installed. The assembly test selects the source for the host OS. A missing toolchain is reported as a test failure with the command that needs to be installed.

## Logging and test results

Every example writes `[INFO] Program started` and, after writing a greeting, `[INFO] Greeting printed` to stderr. Prompts and greetings go to stdout. The launcher also logs the selected language and tool checks to stderr. To save a program's logs:

```sh
./run.sh python 2>program.log
```

Tests verify both the greeting and the runtime log messages. They record test names, commands, input, exit codes, stdout, stderr, failures, and durations in `test_run.log` in this directory. This detailed log is replaced on each run. Commands have a 60-second timeout, with available output logged on timeout.

Each run appends its UTC timestamp, passed/failed/error/skipped counts, exit status, and elapsed time to `test_results.log`. Both log files are ignored by Git. For live test logs too, run:

```sh
python3 -m pytest -q tests --log-cli-level=INFO
```
