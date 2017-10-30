from click.testing import CliRunner
import pytest

from smart_hass import cli

def test_bayes_help():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.bayes)
    assert result.exit_code == 1
    assert 'STDIN' in result.output

    help_result = runner.invoke(cli.bayes, ['--help'])
    assert help_result.exit_code == 0
    assert 'Show this message and exit.' in help_result.output

