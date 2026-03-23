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

    def test_meanness_option_succeeds(self, runner):
        result = runner.invoke(
            cli,
            ["schrodinger", "--meanness", "0.8", "3", "2", "1"],
        )
        assert result.exit_code == 0, result.output

    def test_invalid_meanness_fails(self, runner):
        result = runner.invoke(
            cli,
            ["schrodinger", "--meanness", "1.2", "3", "2", "1"],
        )
        assert result.exit_code != 0


class TestUrinalCommand:
    def test_valid_input_succeeds(self, runner):
        result = runner.invoke(cli, ["urinal", "8", "3", "6", "1", "9", "2"])
        assert result.exit_code == 0, result.output

    def test_no_numbers_fails(self, runner):
        result = runner.invoke(cli, ["urinal"])
        assert result.exit_code != 0

    def test_max_rounds_option_succeeds(self, runner):
        result = runner.invoke(cli, ["urinal", "--max-rounds", "5", "1", "3", "2"])
        assert result.exit_code == 0, result.output

    def test_max_rounds_zero_fails_validation(self, runner):
        result = runner.invoke(cli, ["urinal", "--max-rounds", "0", "1", "3", "2"])
        assert result.exit_code != 0

    def test_awkwardness_option_succeeds(self, runner):
        result = runner.invoke(
            cli,
            ["urinal", "--awkwardness", "0.2", "1", "3", "2"],
        )
        assert result.exit_code == 0, result.output

    def test_awkwardness_out_of_range_fails_validation(self, runner):
        result = runner.invoke(
            cli,
            ["urinal", "--awkwardness", "1.5", "1", "3", "2"],
        )
        assert result.exit_code != 0

    def test_first_entrant_message_no_longer_claims_edge(self, runner):
        result = runner.invoke(cli, ["urinal", "1", "3", "2"])
        assert result.exit_code == 0, result.output
        assert "first in — no neighbours yet" in result.output
        assert "first in — took the edge" not in result.output


class TestListCommand:
    def test_list_succeeds(self, runner):
        result = runner.invoke(cli, ["list"])
        assert result.exit_code == 0, result.output


class TestDigitCommand:
    def test_valid_input_succeeds(self, runner):
        result = runner.invoke(cli, ["digit", "170", "45", "75", "90", "2", "802", "66"])
        assert result.exit_code == 0, result.output

    def test_no_numbers_fails(self, runner):
        result = runner.invoke(cli, ["digit"])
        assert result.exit_code != 0

    def test_output_contains_sorted_result(self, runner):
        result = runner.invoke(cli, ["digit", "3", "1", "2"])
        assert result.exit_code == 0, result.output
        assert "[1, 2, 3]" in result.output

    def test_single_number_succeeds(self, runner):
        result = runner.invoke(cli, ["digit", "42"])
        assert result.exit_code == 0, result.output


class TestRootCommand:
    def test_no_subcommand_succeeds(self, runner):
        result = runner.invoke(cli, [])
        assert result.exit_code == 0, result.output


class TestDarwinCommand:
    def test_valid_input_succeeds(self, runner):
        result = runner.invoke(cli, ["darwin", "3", "1", "2"])
        assert result.exit_code == 0, result.output

    def test_no_numbers_fails(self, runner):
        result = runner.invoke(cli, ["darwin"])
        assert result.exit_code != 0

    def test_max_generations_option_succeeds(self, runner):
        result = runner.invoke(cli, ["darwin", "--max-generations", "50", "2", "1"])
        assert result.exit_code == 0, result.output

    def test_max_generations_zero_fails_validation(self, runner):
        result = runner.invoke(cli, ["darwin", "--max-generations", "0", "2", "1"])
        assert result.exit_code != 0

    def test_population_size_option_succeeds(self, runner):
        result = runner.invoke(cli, ["darwin", "--population-size", "20", "3", "1", "2"])
        assert result.exit_code == 0, result.output

    def test_population_size_one_fails_validation(self, runner):
        result = runner.invoke(cli, ["darwin", "--population-size", "1", "3", "1", "2"])
        assert result.exit_code != 0

    def test_mutation_rate_option_succeeds(self, runner):
        result = runner.invoke(cli, ["darwin", "--mutation-rate", "0.3", "--crossover-rate", "0.7", "3", "1", "2"])
        assert result.exit_code == 0, result.output

    def test_mutation_rate_out_of_range_fails(self, runner):
        result = runner.invoke(cli, ["darwin", "--mutation-rate", "1.5", "3", "1", "2"])
        assert result.exit_code != 0

    def test_crossover_rate_option_succeeds(self, runner):
        result = runner.invoke(cli, ["darwin", "--crossover-rate", "0.8", "--mutation-rate", "0.2", "3", "1", "2"])
        assert result.exit_code == 0, result.output



class TestStalinVisualizeCommand:
    def test_visualize_flag_succeeds(self, runner):
        result = runner.invoke(cli, ["stalin", "-v", "5", "1", "9", "2", "8"])
        assert result.exit_code == 0, result.output

    def test_visualize_long_flag_succeeds(self, runner):
        result = runner.invoke(cli, ["stalin", "--visualize", "3", "1", "2"])
        assert result.exit_code == 0, result.output


class TestDarwinVisualizeCommand:
    def test_visualize_flag_succeeds(self, runner):
        result = runner.invoke(cli, ["darwin", "-v", "3", "1", "2"])
        assert result.exit_code == 0, result.output

    def test_visualize_with_options_succeeds(self, runner):
        result = runner.invoke(cli, [
            "darwin", "-v",
            "--max-generations", "50",
            "--population-size", "20",
            "3", "1", "2",
        ])
        assert result.exit_code == 0, result.output
