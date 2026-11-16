# this_file: tests/test_layout.py
# SPDX-License-Identifier: Apache-2.0
"""Package boundaries preserve public exports, SDK imports and relay entry points."""

import importlib
import subprocess
import sys

import pytest

EXPORTS = {
    "launch": "platforms", "submit_script": "platforms",
    "ScriptSubmission": "platforms", "find_bridge": "platforms",
    "enable_mcp": "host", "setup_mcp": "setup",
    "bridge_parameters": "mcp", "probe_tools": "mcp", "call_tool": "mcp",
    "run_python": "mcp", "execute_script": "mcp", "NativeExecutionError": "mcp",
    "FontLab": "client", "AsyncFontLab": "client",
    "ExecutionResult": "results", "ResultTransportError": "results",
}


def test_public_exports_when_remapped_then_same_names_and_objects():
    import fontlab_remopy

    assert fontlab_remopy.__all__ == list(EXPORTS), "Public export names/order changed"
    for name, module in EXPORTS.items():
        target = importlib.import_module("fontlab_remopy." + module)
        assert getattr(fontlab_remopy, name) is getattr(target, name), name


def test_host_when_imported_then_sdk_and_native_modules_stay_lazy():
    result = subprocess.run(
        [sys.executable, "-c", """
import sys
import fontlab_remopy
assert 'fontlab_remopy.host' not in sys.modules
from fontlab_remopy import enable_mcp
assert enable_mcp.__module__ == 'fontlab_remopy.host'
assert not {'mcp', 'anyio', 'fontlab'} & sys.modules.keys()
"""],
        capture_output=True, text=True, timeout=10, check=False,
    )
    assert result.returncode == 0, result.stderr


def test_mcp_when_nested_then_sdk_is_distinct_and_relay_shim_reexports():
    import mcp as sdk

    from fontlab_remopy import mcp as transport
    from fontlab_remopy import mcp_bridge
    from fontlab_remopy.mcp import relay

    assert sdk is not transport, "Nested transport shadowed the MCP SDK"
    assert transport.ClientSession is sdk.ClientSession, "Wrong ClientSession imported"
    assert mcp_bridge.normalize_result is relay.normalize_result
    assert mcp_bridge.relay is relay.relay
    assert mcp_bridge.main is relay.main
    assert transport.bridge_parameters("bridge").args == [
        "-m", "fontlab_remopy.mcp.relay", "bridge"
    ], "Internal calls must use the canonical relay entry point"


@pytest.mark.parametrize("module", ["mcp.relay", "mcp_bridge"])
def test_relay_when_no_arguments_then_preserves_index_error(module):
    result = subprocess.run(
        [sys.executable, "-m", "fontlab_remopy." + module],
        capture_output=True, text=True, timeout=10, check=False,
    )
    assert result.returncode == 1, result.stderr
    assert result.stderr.rstrip().endswith("IndexError: list index out of range")


@pytest.mark.parametrize("platform", ["linux", "win32"])
def test_platform_when_unsupported_then_launch_errors_name_platform(platform):
    result = subprocess.run(
        [sys.executable, "-c", """
import sys
from pathlib import Path
# Load platform-sensitive stdlib modules before simulating another OS.
import dataclasses, shutil, subprocess
sys.platform = sys.argv[1]
from fontlab_remopy import platforms
from fontlab_remopy import discovery
assert 'fontlab_remopy.platforms.macos' not in sys.modules
assert isinstance(platforms.DEFAULT_APP, Path)
assert platforms.ScriptSubmission(Path('script.flpy')).execution_verified is False
discovery.shutil.which = lambda command: command
assert platforms.find_bridge('explicit bridge') == 'explicit bridge'
for function, args in ((platforms.launch, ()), (platforms.submit_script, ('x.flpy',))):
    try:
        function(*args)
    except NotImplementedError as error:
        assert 'FontLab application launch currently supports macOS' in str(error)
        assert sys.platform in str(error)
    else:
        raise AssertionError('Unsupported launch did not fail')
""", platform],
        capture_output=True, text=True, timeout=10, check=False,
    )
    assert result.returncode == 0, result.stderr


def test_distribution_when_built_then_apache_legal_payloads_are_exact(tmp_path):
    """Check the actual wheel and sdist, including their licence metadata."""
    import tarfile
    import zipfile
    from email.parser import BytesParser
    from pathlib import Path

    root = Path(__file__).resolve().parents[1]
    subprocess.run(["uv", "build", "--out-dir", str(tmp_path), str(root)],
                   check=True, capture_output=True, timeout=120)
    with zipfile.ZipFile(next(tmp_path.glob("*.whl"))) as wheel:
        metadata = BytesParser().parsebytes(wheel.read(next(
            name for name in wheel.namelist() if name.endswith(".dist-info/METADATA"))))
        assert metadata["License-Expression"] == "Apache-2.0"
        assert set(metadata.get_all("License-File")) == {"LICENSE", "NOTICE"}
        for name in ("LICENSE", "NOTICE"):
            member = next(path for path in wheel.namelist()
                          if path.endswith(".dist-info/licenses/" + name))
            assert wheel.read(member) == (root / name).read_bytes()
    with tarfile.open(next(tmp_path.glob("*.tar.gz"))) as archive:
        for name in ("LICENSE", "NOTICE"):
            member = next(path for path in archive.getnames() if path.endswith("/" + name))
            assert archive.extractfile(member).read() == (root / name).read_bytes()
