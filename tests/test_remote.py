# this_file: tests/test_remote.py
# SPDX-License-Identifier: Apache-2.0
"""Launch/file boundaries and native completion/error proofs."""
import json
import sys
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock

import pytest

from fontlab_remopy import enable_mcp, execute_script, launch, mcp, submit_script


def test_missing_app_and_script_fail_before_submission(tmp_path):
    with pytest.raises(FileNotFoundError): launch(tmp_path/'missing.app')
    with pytest.raises(FileNotFoundError): submit_script(tmp_path/'missing.flpy')


def test_submission_with_spaces_is_honestly_unverified(tmp_path,monkeypatch):
    from fontlab_remopy.platforms import macos
    app = tmp_path/'FontLab 9.app';app.mkdir()
    path = tmp_path/'with spaces.flpy';path.write_text('print(42)')
    run = Mock();monkeypatch.setattr(macos.subprocess,'run',run)
    result = submit_script(path,app=app)
    assert result.execution_verified is False
    assert run.call_args.args[0] == ['open','-a',str(app),str(path)]


@pytest.mark.asyncio
async def test_file_execution_proves_native_completion_and_preserves_file_name(tmp_path,monkeypatch):
    path = tmp_path/'script.flpy';path.write_text('print(42)')
    run = AsyncMock(return_value={'success':True,'output':'42'})
    monkeypatch.setattr(mcp,'run_python',run)
    assert (await execute_script(path))['success'] is True
    assert str(path) in run.call_args.args[0] and '__file__' in run.call_args.args[0]


@pytest.mark.asyncio
async def test_native_failure_payload_is_not_transport_success(monkeypatch):
    result = SimpleNamespace(isError=False, content=[SimpleNamespace(type='text',text=json.dumps({'success':False,'error':{'message':'bad code'}}))])
    monkeypatch.setattr(mcp,'call_tool',AsyncMock(return_value=result))
    with pytest.raises(mcp.NativeExecutionError) as error:
        await mcp.run_python('invalid')
    assert error.value.payload['error']['message'] == 'bad code'


def test_enable_mcp_uses_extended_preference_and_not_save(monkeypatch):
    prefs,items = Mock(),Mock()
    monkeypatch.setitem(sys.modules,'fontlab',SimpleNamespace(flPreferences=lambda:prefs,flItems=items))
    enable_mcp()
    prefs.load.assert_called_once_with({'mcp.enabled':True})
    prefs.save.assert_not_called()
    items.notifyPreferencesChanged.assert_called_once_with()


@pytest.mark.asyncio
async def test_invalid_timeout_and_arguments_do_not_open_transport(monkeypatch):
    session = Mock()
    monkeypatch.setattr(mcp,'stdio_client',session)
    with pytest.raises(ValueError,match='positive'):
        await mcp.probe_tools(timeout=0)
    with pytest.raises(TypeError,match='dictionary'):
        await mcp.call_tool('list_fonts',arguments=[])
    session.assert_not_called()


def test_cli_timeout_reports_unknown_execution_outcome(capsys,monkeypatch):
    from fontlab_remopy import cli
    error = TimeoutError('native timeout')
    error.add_note('Setup outcome may be unknown; inspect local status files')
    monkeypatch.setattr(cli,'_perform',AsyncMock(side_effect=error))
    with pytest.raises(SystemExit) as exit:
        cli.main(['setup'])
    assert exit.value.code == 1
    assert 'unknown' in capsys.readouterr().err


def test_grouped_sdk_timeouts_are_identified():
    from fontlab_remopy.cli import _timed_out
    assert _timed_out(ExceptionGroup('SDK', [ExceptionGroup('transport',[TimeoutError()])]))
    assert not _timed_out(ExceptionGroup('SDK',[ValueError('failed')]))
