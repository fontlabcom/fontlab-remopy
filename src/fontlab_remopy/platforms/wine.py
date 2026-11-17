# this_file: src/fontlab_remopy/platforms/wine.py
# SPDX-License-Identifier: Apache-2.0
"""Explicit Wine submission with an existing prefix; scripts must be in drive_c."""

import math
import os
import subprocess
from pathlib import Path, PureWindowsPath

from ..discovery import ScriptSubmission


def _file(path: str | Path) -> Path:
    resolved = Path(path).expanduser().resolve()
    if not resolved.is_file():
        raise FileNotFoundError(resolved)
    return resolved


def _windows(path: Path, prefix: Path) -> str:
    try:
        relative = path.relative_to((prefix / "drive_c").resolve())
    except ValueError as error:
        raise ValueError("File must be inside the selected prefix drive_c") from error
    if any(":" in part or "\\" in part for part in relative.parts):
        raise ValueError("Native filename cannot be represented as a Windows path")
    return str(PureWindowsPath("C:/", *relative.parts))


def _command(
    executable: str | Path, wine: str | Path, prefix: Path, timeout: float
) -> list[str]:
    if not math.isfinite(timeout) or timeout <= 0:
        raise ValueError("timeout must be finite positive seconds")
    launcher = _file(wine)
    if not os.access(launcher, os.X_OK):
        raise PermissionError(f"Wine launcher is not executable: {launcher}")
    if not prefix.is_dir() or not (prefix / "drive_c").is_dir():
        raise FileNotFoundError(prefix / "drive_c")
    return [str(launcher), _windows(_file(executable), prefix)]


def launch(
    executable: str | Path, *, prefix: str | Path, wine: str | Path, timeout: float = 10
) -> None:
    """Request launch in the explicit existing prefix, without retry or readiness proof."""
    root = Path(prefix).expanduser().resolve()
    command = _command(executable, wine, root, timeout)
    subprocess.run(
        command,
        env={**os.environ, "WINEPREFIX": str(root)},
        check=True,
        timeout=timeout,
    )


def submit_script(
    path: str | Path,
    executable: str | Path,
    *,
    prefix: str | Path,
    wine: str | Path,
    timeout: float = 10,
) -> ScriptSubmission:
    """Submit a drive_c script; a return value never proves completed execution."""
    root = Path(prefix).expanduser().resolve()
    command = _command(executable, wine, root, timeout)
    source = _file(path)
    command.append(_windows(source, root))
    subprocess.run(
        command,
        env={**os.environ, "WINEPREFIX": str(root)},
        check=True,
        timeout=timeout,
    )
    return ScriptSubmission(source)
