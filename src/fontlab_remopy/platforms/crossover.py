# this_file: src/fontlab_remopy/platforms/crossover.py
# SPDX-License-Identifier: Apache-2.0
"""Explicit CrossOver submission using the standard macOS bottle directory."""

import subprocess
from pathlib import Path

from ..discovery import ScriptSubmission
from .wine import _command, _file


def _argv(
    executable: str | Path, bottle: str, wine: str | Path, timeout: float
) -> list[str]:
    if not bottle or bottle in {".", ".."} or "/" in bottle or "\\" in bottle:
        raise ValueError(
            "bottle must be a single name in the standard CrossOver Bottles directory"
        )
    root = Path.home() / "Library/Application Support/CrossOver/Bottles" / bottle
    launcher, application = _command(executable, wine, root.resolve(), timeout)
    # Absolute selectors bypass configured bottle search paths (CrossOver CXBottle::find_bottle).
    return [
        launcher,
        "--bottle",
        str(root.resolve()),
        "--no-update",
        "--no-wait",
        "--cx-app",
        application,
    ]


def launch(
    executable: str | Path, *, bottle: str, wine: str | Path, timeout: float = 10
) -> None:
    """Request launch; the bottle must use CrossOver's standard macOS location."""
    subprocess.run(
        _argv(executable, bottle, wine, timeout), check=True, timeout=timeout
    )


def submit_script(
    path: str | Path,
    executable: str | Path,
    *,
    bottle: str,
    wine: str | Path,
    timeout: float = 10,
) -> ScriptSubmission:
    """Submit an existing native file argument without claiming execution completion."""
    command = _argv(executable, bottle, wine, timeout)
    source = _file(path)
    subprocess.run([*command, str(source)], check=True, timeout=timeout)
    return ScriptSubmission(source)
