import logging
import platform
import shlex
import shutil
import subprocess
from pathlib import Path
from time import monotonic

import pytest


HOMEWORK_DIR = Path(__file__).resolve().parents[1]
USER_NAME = "Ada Lovelace"
LOGGER = logging.getLogger("hw_11_hello_worlds")


def run_program(command, *, input_text=f"{USER_NAME}\n", cwd=HOMEWORK_DIR):
    executable = command[0]
    if shutil.which(executable) is None:
        LOGGER.error("Required command is missing: %s", executable)
        pytest.fail(
            f"Required command '{executable}' is missing. "
            "Install the language toolchain described in the homework README."
        )

    LOGGER.info("Command started: %s; stdin=%r", shlex.join(command), input_text)
    started_at = monotonic()
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            input=input_text,
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as error:
        LOGGER.error(
            "Command failed: %s -> exit code %s in %.3fs; stdout=%r; stderr=%r",
            shlex.join(command),
            error.returncode,
            monotonic() - started_at,
            error.stdout,
            error.stderr,
        )
        raise

    LOGGER.info(
        "Command finished: %s -> exit code %s in %.3fs",
        shlex.join(command),
        result.returncode,
        monotonic() - started_at,
    )
    LOGGER.debug("Command output: stdout=%r; stderr=%r", result.stdout, result.stderr)
    return result


def assert_greeting(result):
    LOGGER.info("Checking greeting for %s in stdout=%r", USER_NAME, result.stdout)
    assert result.stdout.startswith("What is your name? ")
    assert result.stdout.rstrip().endswith(f"Hello, {USER_NAME}!")


@pytest.mark.parametrize(
    "language",
    [
        "python",
        "javascript",
        "java",
        "c",
        "cpp",
        "csharp",
        "go",
        "rust",
        "php",
        "ruby",
        "bash",
        "perl",
        "lua",
        "tcl",
        "awk",
        "asm",
    ],
)
def test_program_prompts_for_name_and_greets_user(language, tmp_path):
    if language == "python":
        command = ["python3", str(HOMEWORK_DIR / "hello_world.py")]
    elif language == "javascript":
        command = ["node", str(HOMEWORK_DIR / "hello_world.js")]
    elif language == "java":
        run_program(
            ["javac", "-d", str(tmp_path), str(HOMEWORK_DIR / "HelloWorld.java")]
        )
        command = ["java", "-cp", str(tmp_path), "HelloWorld"]
    elif language == "c":
        binary = tmp_path / "hello_world_c"
        run_program(
            ["cc", str(HOMEWORK_DIR / "hello_world.c"), "-o", str(binary)]
        )
        command = [str(binary)]
    elif language == "cpp":
        binary = tmp_path / "hello_world_cpp"
        run_program(
            ["c++", str(HOMEWORK_DIR / "hello_world.cpp"), "-o", str(binary)]
        )
        command = [str(binary)]
    elif language == "csharp":
        executable = tmp_path / "HelloWorld.exe"
        run_program(
            ["mcs", f"-out:{executable}", str(HOMEWORK_DIR / "HelloWorld.cs")]
        )
        command = ["mono", str(executable)]
    elif language == "go":
        command = ["go", "run", str(HOMEWORK_DIR / "hello_world.go")]
    elif language == "rust":
        binary = tmp_path / "hello_world_rust"
        run_program(
            ["rustc", str(HOMEWORK_DIR / "hello_world.rs"), "-o", str(binary)]
        )
        command = [str(binary)]
    elif language == "php":
        command = ["php", str(HOMEWORK_DIR / "hello_world.php")]
    elif language == "ruby":
        command = ["ruby", str(HOMEWORK_DIR / "hello_world.rb")]
    elif language == "bash":
        command = ["bash", str(HOMEWORK_DIR / "hello_world.sh")]
    elif language == "perl":
        command = ["perl", str(HOMEWORK_DIR / "hello_world.pl")]
    elif language == "lua":
        command = ["lua", str(HOMEWORK_DIR / "hello_world.lua")]
    elif language == "tcl":
        command = ["tclsh", str(HOMEWORK_DIR / "hello_world.tcl")]
    elif language == "awk":
        command = ["awk", "-f", str(HOMEWORK_DIR / "hello_world.awk")]
    else:
        is_macos = platform.system() == "Darwin"
        nasm_source = (
            "hello_world_macos.asm" if is_macos else "hello_world.asm"
        )
        object_file = tmp_path / "hello_world.o"
        binary = tmp_path / "hello_world_asm"

        if is_macos:
            run_program(
                [
                    "nasm",
                    "-f",
                    "macho64",
                    str(HOMEWORK_DIR / nasm_source),
                    "-o",
                    str(object_file),
                ]
            )
            run_program(
                ["clang", "-arch", "x86_64", str(object_file), "-o", str(binary)]
            )
            if platform.machine() == "arm64":
                command = ["arch", "-x86_64", str(binary)]
            else:
                command = [str(binary)]
        else:
            run_program(
                [
                    "nasm",
                    "-f",
                    "elf64",
                    str(HOMEWORK_DIR / nasm_source),
                    "-o",
                    str(object_file),
                ]
            )
            run_program(["ld", str(object_file), "-o", str(binary)])
            command = [str(binary)]

    assert_greeting(run_program(command))
