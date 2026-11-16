# this_file: src/fontlab_remopy/host.py
# SPDX-License-Identifier: Apache-2.0
"""MCP preference setup using the host's verified extended-preference API."""


def enable_mcp(enabled: bool = True) -> None:
    """Run inside FontLab; update only mcp.enabled and notify the host."""
    try:
        import fontlab
    except ModuleNotFoundError as error:
        if error.name == 'fontlab':
            raise RuntimeError('enable_mcp requires execution inside FontLab') from error
        raise
    fontlab.flPreferences().load({'mcp.enabled':enabled})
    fontlab.flItems.notifyPreferencesChanged()
