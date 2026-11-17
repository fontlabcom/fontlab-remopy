# this_file: tests/test_crossover.py
# SPDX-License-Identifier: Apache-2.0
"""Offline command construction proves submission boundaries, not native execution."""

import subprocess
from unittest.mock import Mock

import pytest

from fontlab_remopy import cli


@pytest.fixture
def files(tmp_path, monkeypatch):
    monkeypatch.setenv("HOME", str(tmp_path))
    prefix = tmp_path / "Library/Application Support/CrossOver/Bottles/fontlab"
    exe = prefix / "drive_c/Program Files/Fontlab/FontLab 9.exe"
    exe.parent.mkdir(parents=True)
    exe.write_text("fixture")
    source = prefix / "drive_c/Łódź script.vfpy"
    source.write_text("print(42)")
    launcher = tmp_path / "wine launcher"
    launcher.write_text("fixture")
    launcher.chmod(0o755)
    run = Mock()
    monkeypatch.setattr(subprocess, "run", run)
    return prefix, exe, source, launcher, run


def test_crossover_argv_and_submission(files):
    from fontlab_remopy.platforms import crossover

    prefix, exe, source, launcher, run = files
    result = crossover.submit_script(source, exe, bottle="fontlab", wine=launcher)
    assert result.path == source.resolve() and result.execution_verified is False
    command = [
        str(launcher),
        "--bottle",
        str(prefix),
        "--no-update",
        "--no-wait",
        "--cx-app",
        "C:\\Program Files\\Fontlab\\FontLab 9.exe",
        str(source),
    ]
    run.assert_called_once_with(command, check=True, timeout=10)
    run.reset_mock()
    crossover.launch(exe, bottle="fontlab", wine=launcher, timeout=3)
    run.assert_called_once_with(command[:-1], check=True, timeout=3)


def test_wine_argv_prefix_and_submission(files):
    from fontlab_remopy.platforms import wine

    prefix, exe, source, launcher, run = files
    result = wine.submit_script(source, exe, prefix=prefix, wine=launcher)
    assert result.execution_verified is False
    assert run.call_args.args[0] == [
        str(launcher),
        "C:\\Program Files\\Fontlab\\FontLab 9.exe",
        "C:\\Łódź script.vfpy",
    ]
    assert run.call_args.kwargs["env"]["WINEPREFIX"] == str(prefix)
    assert run.call_args.kwargs["check"] is True
    run.reset_mock()
    wine.launch(exe, prefix=prefix, wine=launcher)
    assert run.call_args.args[0] == [
        str(launcher),
        "C:\\Program Files\\Fontlab\\FontLab 9.exe",
    ]


@pytest.mark.parametrize("backend", ["wine", "crossover"])
@pytest.mark.parametrize("timeout", [0, -1, float("nan"), float("inf"), -float("inf")])
def test_invalid_deadline_never_runs(files, backend, timeout):
    from importlib import import_module

    prefix, exe, source, launcher, run = files
    options = {"prefix": prefix} if backend == "wine" else {"bottle": "fontlab"}
    with pytest.raises(ValueError, match="finite positive"):
        import_module("fontlab_remopy.platforms." + backend).submit_script(
            source, exe, wine=launcher, timeout=timeout, **options
        )
    run.assert_not_called()


@pytest.mark.parametrize("backend", ["wine", "crossover"])
@pytest.mark.parametrize(
    "invalid",
    ["launcher", "launcher_permissions", "prefix", "exe", "source", "outside"],
)
def test_invalid_paths_never_run(files, tmp_path, backend, invalid):
    from importlib import import_module

    prefix, exe, source, launcher, run = files
    if invalid == "launcher":
        launcher.unlink()
    if invalid == "launcher_permissions":
        launcher.chmod(0o644)
    if invalid == "prefix":
        prefix.rename(prefix.with_name("missing"))
    if invalid == "exe":
        exe.unlink()
    if invalid == "source":
        source.unlink()
    if invalid == "outside":
        exe = tmp_path / "outside.exe"
        exe.write_text("fixture")
    options = {"prefix": prefix} if backend == "wine" else {"bottle": "fontlab"}
    with pytest.raises((ValueError, FileNotFoundError, PermissionError)):
        import_module("fontlab_remopy.platforms." + backend).submit_script(
            source, exe, wine=launcher, **options
        )
    run.assert_not_called()


def test_wine_rejects_external_script(files, tmp_path):
    from fontlab_remopy.platforms import wine

    prefix, exe, _, launcher, run = files
    source = tmp_path / "external.vfpy"
    source.write_text("fixture")
    with pytest.raises(ValueError, match="drive_c"):
        wine.submit_script(source, exe, prefix=prefix, wine=launcher)
    run.assert_not_called()


@pytest.mark.parametrize(
    "bottle", ["", "../fontlab", "/tmp/fontlab", ".", "a/b", "a\\b"]
)
def test_crossover_rejects_ambiguous_selector(files, bottle):
    from fontlab_remopy.platforms import crossover

    _, exe, _, launcher, run = files
    with pytest.raises(ValueError, match="bottle"):
        crossover.launch(exe, bottle=bottle, wine=launcher)
    run.assert_not_called()


@pytest.mark.parametrize("backend", ["wine", "crossover"])
@pytest.mark.parametrize("operation", ["submit", "launch"])
def test_cli_dispatch_and_honest_result(files, capsys, backend, operation):
    prefix, exe, source, launcher, run = files
    args = [operation] + ([str(source)] if operation == "submit" else [])
    args += ["--backend", backend, "--executable", str(exe), "--wine", str(launcher)]
    args += ["--prefix", str(prefix)] if backend == "wine" else ["--bottle", "fontlab"]
    assert cli.main(args) == 0
    output = capsys.readouterr().out
    assert (
        '"execution_verified": false'
        if operation == "submit"
        else '"launch_requested": true'
    ) in output
    run.assert_called_once()


@pytest.mark.parametrize(
    "extra",
    [
        [],
        ["--backend", "wine"],
        ["--backend", "crossover"],
        ["--bottle", "fontlab"],
        ["--prefix", "x"],
    ],
)
def test_cli_incomplete_configuration_never_runs(files, extra):
    *_, run = files
    # Empty options preserve the existing macOS launch; test submit's missing source instead.
    args = ["submit", "/nonexistent/script.vfpy"] + extra
    with pytest.raises(SystemExit):
        cli.main(args)
    run.assert_not_called()


@pytest.mark.parametrize("operation", ["launch", "submit"])
@pytest.mark.parametrize(
    "error",
    [subprocess.TimeoutExpired("wine", 1), subprocess.CalledProcessError(2, "wine")],
)
def test_cli_process_failure_does_not_retry(files, capsys, operation, error):
    _, exe, source, launcher, run = files
    run.side_effect = error
    args = [operation] + ([str(source)] if operation == "submit" else [])
    args += [
        "--backend",
        "crossover",
        "--executable",
        str(exe),
        "--wine",
        str(launcher),
        "--bottle",
        "fontlab",
    ]
    with pytest.raises(SystemExit) as result:
        cli.main(args)
    assert result.value.code == 1
    assert ("unknown" in capsys.readouterr().err) == isinstance(
        error, subprocess.TimeoutExpired
    )
    run.assert_called_once()


def test_crossover_accepts_external_native_script(files, tmp_path):
    from fontlab_remopy.platforms import crossover

    _, exe, _, launcher, run = files
    source = tmp_path / "Łódź external.vfpy"
    source.write_text("fixture")
    result = crossover.submit_script(source, exe, bottle="fontlab", wine=launcher)
    assert result.path == source.resolve()
    assert run.call_args.args[0][-1] == str(source)


@pytest.mark.parametrize(
    "extra",
    [
        ["--backend", "crossover", "--prefix", "prefix"],
        ["--backend", "wine", "--bottle", "fontlab"],
        ["--backend", "macos", "--wine", "wine"],
        ["--backend", "wine", "--bottle", "fontlab", "--prefix", "prefix"],
    ],
)
def test_cli_conflicting_backend_options_never_run(files, extra):
    _, exe, _, launcher, run = files
    with pytest.raises(SystemExit):
        cli.main(["launch", "--executable", str(exe), "--wine", str(launcher), *extra])
    run.assert_not_called()


@pytest.mark.parametrize("operation", ["launch", "submit"])
def test_cli_keeps_macos_default(files, monkeypatch, capsys, operation):
    from fontlab_remopy import platforms
    from fontlab_remopy.discovery import ScriptSubmission

    _, _, source, _, run = files
    launch = Mock()
    submit = Mock(return_value=ScriptSubmission(source))
    monkeypatch.setattr(platforms, "launch", launch)
    monkeypatch.setattr(platforms, "submit_script", submit)
    assert cli.main([operation] + ([str(source)] if operation == "submit" else [])) == 0
    if operation == "launch":
        launch.assert_called_once_with(timeout=30)
    else:
        submit.assert_called_once_with(source, timeout=30)
        assert '"execution_verified": false' in capsys.readouterr().out
    run.assert_not_called()


@pytest.mark.parametrize("name", ["D:other.exe", r"other\file.exe"])
def test_native_filename_cannot_change_windows_drive_or_components(files, name):
    from fontlab_remopy.platforms import wine

    prefix, _, _, launcher, run = files
    exe = prefix / "drive_c" / name
    exe.write_text("fixture")
    with pytest.raises(ValueError, match="Windows"):
        wine.launch(exe, prefix=prefix, wine=launcher)
    run.assert_not_called()
