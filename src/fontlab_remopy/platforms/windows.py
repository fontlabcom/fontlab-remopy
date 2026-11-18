# this_file: src/fontlab_remopy/platforms/windows.py
# SPDX-License-Identifier: Apache-2.0
"""Request native Windows application launch and script submission."""

import math
import subprocess
import sys
from pathlib import Path

from ..discovery import DEFAULT_APP, ScriptSubmission


def _start(app: str | Path, timeout: float, *arguments: str) -> None:
    if not math.isfinite(timeout) or timeout <= 0:
        raise ValueError('Launch timeout must be positive and finite')
    executable = Path(app).expanduser().resolve()
    if not executable.is_file():
        raise FileNotFoundError(executable)
    if sys.platform != 'win32':
        raise NotImplementedError('Native Windows launch requires Windows')
    subprocess.Popen([str(executable), *arguments])


def launch(app: str | Path = DEFAULT_APP, timeout: float = 10) -> None:
    """Request launch without waiting for the desktop application's lifetime."""
    _start(app, timeout)


def submit_script(
    path: str | Path, app: str | Path = DEFAULT_APP, timeout: float = 10
) -> ScriptSubmission:
    """Submit one file to FontLab without claiming completed execution."""
    source = Path(path).expanduser().resolve()
    if not source.is_file():
        raise FileNotFoundError(source)
    _start(app, timeout, str(source))
    return ScriptSubmission(source)
