# this_file: src/fontlab_remopy/actions.py
# SPDX-License-Identifier: Apache-2.0
"""Named native tool calls shared by synchronous and asynchronous clients."""

from collections.abc import Callable
from typing import Any


class Controls:
    """Named catalogue calls; async clients return awaitable values.

    Each method calls one native MCP tool by name and returns its JSON payload;
    keyword arguments are the tool's own parameters (see ``tools()`` for schemas).
    Methods that change FontLab state perform the operation immediately.
    """

    def list_fonts(self) -> Any:
        """Call ``list_fonts``: every open font, as ``{"fonts": [...]}``."""
        return self.tool("list_fonts")

    def current_font(self) -> Any:
        """Call ``get_active_font``: the font in the active window."""
        return self.tool("get_active_font")

    def current_glyphs(self) -> Any:
        """Call ``get_current_glyphs``: the glyphs of the active window."""
        return self.tool("get_current_glyphs")

    def font_info(self, **arguments: Any) -> Any:
        """Call ``get_font_info`` with the tool's arguments."""
        return self.tool("get_font_info", **arguments)

    def glyph_info(self, **arguments: Any) -> Any:
        """Call ``get_glyph`` with the tool's arguments."""
        return self.tool("get_glyph", **arguments)

    def glyph(self, name: str, **arguments: Any) -> Any:
        """Call ``get_glyph`` for the glyph called ``name``."""
        return self.glyph_info(glyph_name=name, **arguments)

    def list_glyphs(self, **arguments: Any) -> Any:
        """Call ``list_glyphs`` with the tool's arguments."""
        return self.tool("list_glyphs", **arguments)

    def font_metrics(self, **arguments: Any) -> Any:
        """Call ``get_font_metrics`` with the tool's arguments."""
        return self.tool("get_font_metrics", **arguments)

    def glyph_metrics(self, **arguments: Any) -> Any:
        """Call ``get_glyph_metrics`` with the tool's arguments."""
        return self.tool("get_glyph_metrics", **arguments)

    def list_actions(self) -> Any:
        """Call ``list_actions``: the application actions that ``run_actions`` accepts."""
        return self.tool("list_actions")

    def run_actions(self, **arguments: Any) -> Any:
        """Call ``run_actions``: run application actions. Changes FontLab state."""
        return self.tool("run_actions", **arguments)

    def output(self, **arguments: Any) -> Any:
        """Call ``get_python_output``: recent Python output captured by the MCP tool."""
        return self.tool("get_python_output", **arguments)

    def open_font(self, **arguments: Any) -> Any:
        """Call ``open_font``. Opens a font in FontLab."""
        return self.tool("open_font", **arguments)

    def new_font(self, **arguments: Any) -> Any:
        """Call ``new_font``. Creates an empty font in FontLab."""
        return self.tool("new_font", **arguments)

    def save_font(self, **arguments: Any) -> Any:
        """Call ``save_font``. Writes the font to disk."""
        return self.tool("save_font", **arguments)

    def close_font(self, **arguments: Any) -> Any:
        """Call ``close_font``. Closes a font in FontLab."""
        return self.tool("close_font", **arguments)

    def activate_font(self, **arguments: Any) -> Any:
        """Call ``set_active_font``. Changes which font is active."""
        return self.tool("set_active_font", **arguments)

    def activate_glyph(self, **arguments: Any) -> Any:
        """Call ``set_active_glyph``. Changes which glyph is active."""
        return self.tool("set_active_glyph", **arguments)

    def set_font_metrics(self, **arguments: Any) -> Any:
        """Call ``set_font_metrics``. Changes font metrics."""
        return self.tool("set_font_metrics", **arguments)

    def set_glyph_metrics(self, **arguments: Any) -> Any:
        """Call ``set_glyph_metrics``. Changes glyph metrics."""
        return self.tool("set_glyph_metrics", **arguments)

    def python(self, function: Callable) -> Callable:
        """Decorate a normal function to execute remotely with JSON values."""
        from .remote import remote_function

        return remote_function(self, function)
