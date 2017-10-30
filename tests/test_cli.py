from click.testing import CliRunner
import pytest

from smart_hass import cli

def test_bayes_help():
    """Test the CLI."""
    runner = CliRunner()

    help_result = runner.invoke(cli.bayes, ['--help'])
    assert help_result.exit_code == 0
    assert 'Show this message and exit.' in help_result.output

