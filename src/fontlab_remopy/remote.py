# this_file: src/fontlab_remopy/remote.py
# SPDX-License-Identifier: Apache-2.0
"""Transmit inspectable ordinary Python functions, with explicit capture rules."""

from __future__ import annotations

import ast
import inspect
import textwrap
from collections.abc import Callable
from functools import wraps
from typing import Any
from uuid import uuid4


def remote_function(client: Any, function: Callable) -> Callable:
    """Bind a real signature; imports belong inside the remote function.

    Globals and closure values are deliberately unsupported. Native objects are
    created/imported remotely; only JSON arguments and results cross the bridge.
    """
    if not inspect.isfunction(function) or inspect.iscoroutinefunction(function):
        raise ValueError(
            "Remote python requires an ordinary synchronous Python function"
        )
    captures = inspect.getclosurevars(function)
    if captures.nonlocals or captures.globals:
        raise ValueError(
            "Remote functions cannot capture globals or closure values; import inside the body"
        )
    try:
        tree = ast.parse(textwrap.dedent(inspect.getsource(function)))
    except (OSError, TypeError, SyntaxError) as error:
        raise ValueError(
            "Remote function source is unavailable; use run/eval in this environment"
        ) from error
    if len(tree.body) != 1 or not isinstance(tree.body[0], ast.FunctionDef):
        raise ValueError("Remote source must contain one ordinary function")
    definition = tree.body[0]
    definition.decorator_list = []
    # Default values are bound locally and transported as JSON. Evaluate neither
    # default expressions nor annotation names in the isolated host namespace.
    definition.args.defaults = []
    definition.args.kw_defaults = [None for _ in definition.args.kw_defaults]
    definition.returns = None
    for arg in [
        *definition.args.posonlyargs,
        *definition.args.args,
        *definition.args.kwonlyargs,
    ]:
        arg.annotation = None
    if definition.args.vararg:
        definition.args.vararg.annotation = None
    if definition.args.kwarg:
        definition.args.kwarg.annotation = None
    source = ast.unparse(tree)
    signature = inspect.signature(function)

    @wraps(function)
    def invoke(*args, **kwargs):
        bound = signature.bind(*args, **kwargs)
        bound.apply_defaults()
        return _invoke(client, source, function.__name__, bound)

    return invoke


def _invoke(client: Any, source: str, name: str, bound: inspect.BoundArguments) -> Any:
    args_name = "_remopy_args_" + uuid4().hex
    kwargs_name = "_remopy_kwargs_" + uuid4().hex
    variables = {args_name: list(bound.args), kwargs_name: bound.kwargs}
    code = source + f"\nresult = {name}(*{args_name}, **{kwargs_name})"
    if inspect.iscoroutinefunction(client.run):

        async def await_value():
            return (await client.run(code, **variables)).value

        return await_value()
    return client.run(code, **variables).value
