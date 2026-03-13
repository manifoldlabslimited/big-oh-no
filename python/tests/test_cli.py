import pytest
from click.testing import CliRunner

from big_oh_no.cli import cli


@pytest.fixture
def runner():
    return CliRunner()


class TestStalinCommand:
    def test_valid_input_succeeds(self, runner):
        result = runner.invoke(cli, ["stalin", "5", "1", "9", "2", "8"])
        assert result.exit_code == 0, result.output

    def test_already_sorted_succeeds(self, runner):
        result = runner.invoke(cli, ["stalin", "1", "2", "3"])
        assert result.exit_code == 0, result.output

    def test_no_numbers_fails(self, runner):
        result = runner.invoke(cli, ["stalin"])
        assert result.exit_code != 0


class TestLinusCommand:
    def test_valid_input_succeeds(self, runner):
        result = runner.invoke(cli, ["linus", "3", "1", "7", "2"])
        assert result.exit_code == 0, result.output

    def test_already_sorted_succeeds(self, runner):
        result = runner.invoke(cli, ["linus", "1", "2", "3"])
        assert result.exit_code == 0, result.output

    def test_no_numbers_fails(self, runner):
        result = runner.invoke(cli, ["linus"])
        assert result.exit_code != 0


class TestWaitCommand:
    def test_valid_input_succeeds(self, runner):
        result = runner.invoke(cli, ["wait", "1"])
        assert result.exit_code == 0, result.output

    def test_no_numbers_fails(self, runner):
        result = runner.invoke(cli, ["wait"])
        assert result.exit_code != 0


class TestBogoCommand:
    def test_valid_input_succeeds(self, runner):
        result = runner.invoke(cli, ["bogo", "1"])
        assert result.exit_code == 0, result.output

    def test_no_numbers_fails(self, runner):
        result = runner.invoke(cli, ["bogo"])
        assert result.exit_code != 0

    def test_max_attempts_option_succeeds(self, runner):
        result = runner.invoke(cli, ["bogo", "--max-attempts", "5", "1"])
        assert result.exit_code == 0, result.output

    def test_max_attempts_zero_fails_validation(self, runner):
        result = runner.invoke(cli, ["bogo", "--max-attempts", "0", "1"])
        assert result.exit_code != 0


class TestSchrodingerCommand:
    def test_valid_input_succeeds(self, runner):
        result = runner.invoke(cli, ["schrodinger", "3", "2", "1"])
        assert result.exit_code == 0, result.output

    def test_no_numbers_fails(self, runner):
        result = runner.invoke(cli, ["schrodinger"])
        assert result.exit_code != 0

    def test_already_sorted_input_succeeds(self, runner):
        # Already-sorted input deterministically collapses to unsorted — still exits 0.
        result = runner.invoke(cli, ["schrodinger", "1", "2", "3"])
        assert result.exit_code == 0, result.output


class TestListCommand:
    def test_list_succeeds(self, runner):
        result = runner.invoke(cli, ["list"])
        assert result.exit_code == 0, result.output


class TestRootCommand:
    def test_no_subcommand_succeeds(self, runner):
        result = runner.invoke(cli, [])
        assert result.exit_code == 0, result.output
