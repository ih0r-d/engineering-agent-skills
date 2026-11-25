#!/usr/bin/env python3
"""Run the installer from its historical path."""

from pathlib import Path
from runpy import run_path


if __name__ == "__main__":
    run_path(str(Path(__file__).resolve().parents[1] / ".scripts/skills.py"), run_name="__main__")
