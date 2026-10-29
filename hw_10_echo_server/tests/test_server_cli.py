from pathlib import Path
import subprocess
import sys

import pytest


SERVER_PATH = Path(__file__).resolve().parents[1] / "server.py"


def test_help_describes_port_option_without_starting_server():
    result = subprocess.run(
        [sys.executable, str(SERVER_PATH), "--help"],
        capture_output=True,
        text=True,
        timeout=5,
    )

    assert result.returncode == 0
    assert "--port" in result.stdout
    assert "Start an echo HTTP server" in result.stdout
    assert result.stderr == ""


@pytest.mark.parametrize("arguments", [["--port", "invalid"], ["--port"], ["--unknown-option"]])
def test_invalid_arguments_exit_with_usage_error_without_starting_server(arguments):
    result = subprocess.run(
        [sys.executable, str(SERVER_PATH), *arguments],
        capture_output=True,
        text=True,
        timeout=5,
    )

    assert result.returncode == 2
    assert "usage:" in result.stderr
    assert "error:" in result.stderr
    assert "Started on" not in result.stdout
