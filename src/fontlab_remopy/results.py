# this_file: src/fontlab_remopy/results.py
# SPDX-License-Identifier: Apache-2.0
"""Explicit JSON transport for remote Python values and captured streams."""

from __future__ import annotations

import json
import keyword
from dataclasses import dataclass
from typing import Any
from uuid import uuid4

from .mcp import NativeExecutionError

MAX_CODE_BYTES = 32768
MAX_OUTPUT_BYTES = 65536


class ResultTransportError(RuntimeError):
    """Execution may have completed, but its JSON result cannot be recovered."""


@dataclass(frozen=True)
class ExecutionResult:
    """A JSON-native value plus the script's separate Python output streams."""

    value: Any
    stdout: str
    stderr: str


def encode_execution(
    source: str, variables: dict[str, Any], filename: str
) -> tuple[str, str]:
    """Bind JSON data into an isolated namespace, never interpolate it as code."""
    for name in variables:
        if not name.isidentifier() or keyword.iskeyword(name) or name.startswith("__"):
            raise ValueError(f"Invalid remote variable name: {name!r}")
    encoded = json.dumps(variables, ensure_ascii=False, allow_nan=False)
    nonce = uuid4().hex
    # This helper executes in its own globals. User code gets a second isolated
    # dictionary, so even imports cannot overwrite transport helpers.
    helper = f"""import contextlib, io, json, traceback, importlib
namespace = {{}}
for module_name in ('fontlab', 'fontgate', 'fontpr', 'PythonQt'):
    try:
        namespace[module_name] = importlib.import_module(module_name)
    except ModuleNotFoundError as error:
        if error.name != module_name:
            raise
namespace.update(json.loads({encoded!r}))
namespace.update(__name__='__main__', __file__={filename!r})
out, err = io.StringIO(), io.StringIO()
failure = None
with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
    try:
        exec(compile({source!r}, {filename!r}, 'exec'), namespace)
    except BaseException as error:
        failure = {{'type': type(error).__name__, 'message': str(error), 'traceback': traceback.format_exc()}}
envelope = {{'nonce': {nonce!r}, 'value': namespace.get('result'), 'stdout': out.getvalue(), 'stderr': err.getvalue(), 'error': failure}}
try:
    encoded = json.dumps(envelope, ensure_ascii=False, allow_nan=False)
except (TypeError, ValueError) as error:
    encoded = json.dumps({{'nonce': {nonce!r}, 'transport_error': 'Result is not JSON serializable: ' + str(error)}})
if len(encoded.encode('utf-8')) > {MAX_OUTPUT_BYTES - 100}:
    encoded = json.dumps({{'nonce': {nonce!r}, 'transport_error': 'Result/output exceeds native 65536-byte output limit'}})
print({("FONTLAB_REMOPY_" + nonce + ":")!r} + encoded)
"""
    code = f"exec({helper!r}, {{}})"
    if len(code.encode("utf-8")) > MAX_CODE_BYTES:
        raise ValueError(
            "Remote Python exceeds native 32768-byte code limit including JSON transport"
        )
    return code, nonce


def decode_execution(payload: dict[str, Any], nonce: str) -> ExecutionResult:
    """Require a complete, unique nonce-matched envelope; truncation is an error."""
    if not payload.get("success"):
        raise NativeExecutionError(payload)
    marker = "FONTLAB_REMOPY_" + nonce + ":"
    # The helper frames with LF. Unicode line separators are valid JSON string
    # contents when ensure_ascii=False, so str.splitlines() would corrupt them.
    lines = [
        line[len(marker) :]
        for line in payload.get("output", "").split("\n")
        if line.startswith(marker)
    ]
    if len(lines) != 1:
        raise ResultTransportError(
            "Remote result envelope missing or ambiguous; execution outcome may be unknown"
        )
    try:
        envelope = json.loads(lines[0])
    except (ValueError, TypeError) as error:
        raise ResultTransportError(
            "Incomplete remote JSON result; execution outcome may be unknown"
        ) from error
    if not isinstance(envelope, dict) or envelope.get("nonce") != nonce:
        raise ResultTransportError("Remote result nonce mismatch")
    if envelope.get("transport_error"):
        raise ResultTransportError(envelope["transport_error"])
    if envelope.get("error"):
        raise NativeExecutionError(envelope)
    if not {"value", "stdout", "stderr"}.issubset(envelope) or not all(
        isinstance(envelope[name], str) for name in ("stdout", "stderr")
    ):
        raise ResultTransportError("Incomplete remote result envelope")
    return ExecutionResult(envelope["value"], envelope["stdout"], envelope["stderr"])
