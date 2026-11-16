# this_file: src/fontlab_remopy/platforms/macos/__init__.py
# SPDX-License-Identifier: Apache-2.0
"""macOS application launch and file-association submission."""

import subprocess
import sys
from pathlib import Path

from ...discovery import DEFAULT_APP, ScriptSubmission, find_bridge

__all__ = ["DEFAULT_APP", "ScriptSubmission", "find_bridge", "launch", "submit_script"]


def _app(app: str | Path) -> Path:
    path = Path(app).expanduser().resolve()
    if not path.is_dir():
        raise FileNotFoundError(path)
    if sys.platform != 'darwin':
        raise NotImplementedError('FontLab application launch currently supports macOS')
    return path


def launch(app: str | Path = DEFAULT_APP, timeout: float = 10) -> None:
    """Request launch; native MCP discovery is the readiness check."""
    subprocess.run(['open','-a',str(_app(app))],check=True,timeout=timeout)


def submit_script(path: str | Path, app: str | Path = DEFAULT_APP, timeout: float = 10) -> ScriptSubmission:
    """Request file-association execution without claiming completed execution."""
    source = Path(path).expanduser().resolve()
    if not source.is_file():
        raise FileNotFoundError(source)
    subprocess.run(['open','-a',str(_app(app)),str(source)],check=True,timeout=timeout)
    return ScriptSubmission(source)
