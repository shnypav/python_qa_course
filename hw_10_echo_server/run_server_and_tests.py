#!/usr/bin/env python3
from pathlib import Path
import subprocess
import sys


def main():
    homework_dir = Path(__file__).resolve().parent
    return subprocess.call(
        [sys.executable, "-m", "pytest", str(homework_dir / "tests"), *sys.argv[1:]],
        cwd=homework_dir,
    )


if __name__ == "__main__":
    sys.exit(main())
