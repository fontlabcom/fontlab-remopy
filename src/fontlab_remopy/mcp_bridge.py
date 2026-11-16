# this_file: src/fontlab_remopy/mcp_bridge.py
# SPDX-License-Identifier: Apache-2.0
"""Deprecated compatibility entry point; use fontlab_remopy.mcp.relay."""

# Saved external MCP configs may still run `python -m fontlab_remopy.mcp_bridge`.
# The warning goes to stderr (the warnings module default), never stdout,
# because stdout carries the MCP stdio protocol.
import warnings

from .mcp.relay import main, normalize_result, relay

# Under `-m` this module is __main__, and the default filters show
# DeprecationWarning only when it is attributed to __main__.
warnings.warn(
    "fontlab_remopy.mcp_bridge is deprecated; use fontlab_remopy.mcp.relay",
    DeprecationWarning,
    stacklevel=1 if __name__ == "__main__" else 2,
)

__all__ = ["normalize_result", "relay", "main"]  # noqa: RUF022 - preserve compatibility export order


if __name__ == "__main__":
    main()
