#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_satellite_populate
----------------------------------

Tests for `satellite_populate` module.
"""

import os
import tempfile

from click.testing import CliRunner
from satellite_populate import commands

runner = CliRunner()
_test_dir = os.path.dirname(__file__)


def _config_setup(monkeypatch):
    monkeypatch.delenv(commands.SATELLITE_POPULATE_FILE, False)
    monkeypatch.setenv('HOME', _test_dir)


def test_invoked_with_no_datafile_shows_help():
    result = runner.invoke(commands.main, ['--no-output'])
    assert result.exit_code == 0
    assert 'https://satellite-populate.readthedocs.io' in result.output


def test_help_output():
    help_result = runner.invoke(commands.main, ['--help'])
    assert help_result.exit_code == 0
    assert 'https://satellite-populate.readthedocs.io' in help_result.output


def test_raises_with_invalid_path():
    result = runner.invoke(commands.main, ['/foo/baz/zaz.yaml'])
    assert result.exit_code == -1


def test_raises_with_invalid_extension():
    result = runner.invoke(commands.main, ['/foo/baz/zaz.txt'])
    assert result.exit_code == -1


def test_validate_raise_validation_exit_status():
    yaml = (
        "actions: ["
        "{'action': 'assertion', 'operator': 'eq', 'data': [1, 2]}"
        "]"
    )
    mode = '--mode=validate'
    result = runner.invoke(commands.main, [yaml, mode, '--no-output'])
    assert result.exit_code == 1
    assert 'System entities did not validated!' in result.output
    assert '1 is NOT eq to 2' in result.output


def test_populate_do_not_raise_validation_exit_status():
    yaml = (
        "actions: ["
        "{'action': 'assertion', 'operator': 'eq', 'data': [1, 2]}"
        "]"
    )
    result = runner.invoke(commands.main, [yaml, '--no-output'])
    assert result.exit_code == 0
    assert 'System entities did not validated!' not in result.output
    assert '1 is NOT eq to 2' in result.output


def test_config_no_file(monkeypatch):
    _config_setup(monkeypatch)
    assert commands.SATELLITE_POPULATE_FILE not in os.environ.keys()
    assert commands.CONFIG_FILE not in os.listdir(os.environ['HOME'])
    result = commands.configure()
    assert result == {}


def test_config_file(monkeypatch):
    _config_setup(monkeypatch)
    config_file = os.path.join(os.environ['HOME'], commands.CONFIG_FILE)
    with tempfile.NamedTemporaryFile(mode='w', dir=_test_dir) as temp:
        temp.write('hostname: test.com')
        os.link(temp.name, config_file)
    result = commands.configure()
    assert result == {'hostname': 'test.com'}
    os.remove(config_file)


def test_config_env(monkeypatch):
    _config_setup(monkeypatch)
    temp = tempfile.NamedTemporaryFile(mode='w', suffix='.yaml')
    monkeypatch.setenv(commands.SATELLITE_POPULATE_FILE, temp.name)
    temp.write('username: dbrownjr')
    temp.flush()
    result = commands.configure()
    temp.close()
    assert not os.path.isfile(
        os.path.join(os.environ['HOME'], commands.CONFIG_FILE)
    )
    assert result == {'username': 'dbrownjr'}


def test_config_file_before_env(monkeypatch):
    _config_setup(monkeypatch)
    # env_var
    env_var = tempfile.NamedTemporaryFile(mode='w', suffix='.yaml')
    monkeypatch.setenv(commands.SATELLITE_POPULATE_FILE, env_var.name)
    env_var.write('hostname: environment.variable.com')
    env_var.flush()
    # config_file
    config_file = os.path.join(os.environ['HOME'], commands.CONFIG_FILE)
    with tempfile.NamedTemporaryFile(mode='w', dir=_test_dir) as temp:
        temp.write('hostname: config.file.com')
        os.link(temp.name, config_file)
    assert os.path.isfile(
        os.path.join(os.environ['HOME'], commands.CONFIG_FILE)
    )
    assert os.environ[commands.SATELLITE_POPULATE_FILE] == env_var.name
    result = commands.configure()
    assert result['hostname'] == 'config.file.com'
    env_var.close()
    os.remove(config_file)
