# this_file: src/fontlab_remopy/platforms/__init__.py
# SPDX-License-Identifier: Apache-2.0
"""Select application launch support while retaining portable bridge discovery."""

import sys
from pathlib import Path

from ..discovery import DEFAULT_APP, ScriptSubmission, find_bridge

__all__ = ["DEFAULT_APP", "ScriptSubmission", "find_bridge", "launch", "submit_script"]

if sys.platform == "darwin":
    from .macos import launch, submit_script
elif sys.platform == "win32":
    from .windows import launch, submit_script
else:
    def launch(app: str | Path = DEFAULT_APP, timeout: float = 10) -> None:
        """Report unsupported native application launch on this platform."""
        raise NotImplementedError(
            f"FontLab application launch currently supports macOS (platform: {sys.platform})"
        )

    def submit_script(
        path: str | Path, app: str | Path = DEFAULT_APP, timeout: float = 10
    ) -> ScriptSubmission:
        """Report unsupported file-association submission on this platform."""
        raise NotImplementedError(
            f"FontLab application launch currently supports macOS (platform: {sys.platform})"
        )
