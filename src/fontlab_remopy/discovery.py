# this_file: src/fontlab_remopy/discovery.py
# SPDX-License-Identifier: Apache-2.0
"""Portable bridge discovery and application submission data."""

import os
import shutil
from dataclasses import dataclass
from pathlib import Path

DEFAULT_APP = Path("/Applications/FontLab 9.app")


@dataclass(frozen=True)
class ScriptSubmission:
    path: Path
    execution_verified: bool = False


def find_bridge(command: str | Path | None = None) -> str | None:
    """Find an executable without splitting paths containing spaces."""
    override = command or os.environ.get('FONTLAB_MCP_COMMAND') or os.environ.get('AIDUS_FONTLAB_MCP_COMMAND')
    if override:
        return shutil.which(str(Path(override).expanduser()))
    candidates = [shutil.which('fontlab-mcp'), str(DEFAULT_APP/'Contents/MacOS/fontlab-mcp'),
                  str(Path.home()/'Applications/FontLab 9.app/Contents/MacOS/fontlab-mcp')]
    return next((path for path in candidates if path and os.access(path,os.X_OK)),None)
