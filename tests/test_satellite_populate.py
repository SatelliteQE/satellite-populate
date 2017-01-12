#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_satellite_populate
----------------------------------

Tests for `satellite_populate` module.
"""

from click.testing import CliRunner
from satellite_populate import commands

runner = CliRunner()


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
