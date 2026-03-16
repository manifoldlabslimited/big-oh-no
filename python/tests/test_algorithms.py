import numpy as np
import pytest
from pydantic import ValidationError

from big_oh_no import bogo_sort
from big_oh_no import digit_sort
from big_oh_no import darwin_sort
from big_oh_no import linus_sort
from big_oh_no import schrodinger_sort
from big_oh_no import stalin_sort
from big_oh_no import urinal_sort
from big_oh_no import wait_sort


def test_stalin_sort_outputs_survivors_and_eliminated(monkeypatch):
    monkeypatch.setattr(stalin_sort.time, "sleep", lambda _: None)
    survivors, eliminated = stalin_sort.stalin_sort([5, 1, 9, 2, 8])

    assert survivors == [5, 9]
    assert eliminated == [1, 2, 8]


def test_linus_sort_outputs_approved_and_rejected(monkeypatch):
    monkeypatch.setattr(linus_sort.time, "sleep", lambda _: None)
    monkeypatch.setattr(linus_sort.random, "choice", lambda seq: seq[0])

    approved, rejected = linus_sort.linus_sort([3, 1, 7, 2])

    assert approved == [3, 7]
    assert rejected == [1, 2]


def test_wait_sort_handles_duplicate_values(monkeypatch):
    monkeypatch.setattr(wait_sort.time, "sleep", lambda _: None)
    sorted_nums, _ = wait_sort.wait_sort([2, 1, 2])

    assert len(sorted_nums) == 3
    assert len(wait_sort.completions) == len(sorted_nums)


def test_bogo_sort_returns_sorted_list(monkeypatch):
    # Force deterministic progress to keep the test fast and stable.
    monkeypatch.setattr(bogo_sort.random, "shuffle", lambda values: values.sort())

    sorted_nums, attempts, _ = bogo_sort.bogo_sort([3, 1, 2], max_attempts=5)

    assert sorted_nums == [1, 2, 3]
    assert attempts == 1


def test_schrodinger_sort_always_destroys_already_sorted_input(monkeypatch):
    monkeypatch.setattr(schrodinger_sort.time, "sleep", lambda _: None)
    monkeypatch.setattr(schrodinger_sort.random, "choice", lambda seq: seq[0])
    monkeypatch.setattr(schrodinger_sort.random, "shuffle", lambda lst: lst.reverse())

    result, collapsed_to_sorted, _ = schrodinger_sort.schrodinger_sort([1, 2, 3])

    assert collapsed_to_sorted is False
    assert result != [1, 2, 3]


def test_schrodinger_sort_collapses_to_sorted_when_random_cooperates(monkeypatch):
    monkeypatch.setattr(schrodinger_sort.time, "sleep", lambda _: None)
    monkeypatch.setattr(schrodinger_sort.random, "choice", lambda seq: seq[0])
    monkeypatch.setattr(schrodinger_sort.random, "shuffle", lambda lst: lst.reverse())
    monkeypatch.setattr(schrodinger_sort.random, "random", lambda: 0.0)  # < 0.5 → sorted

    result, collapsed_to_sorted, _ = schrodinger_sort.schrodinger_sort([3, 1, 2])

    assert collapsed_to_sorted is True
    assert result == [1, 2, 3]


def test_schrodinger_low_meanness_favors_sorted(monkeypatch):
    monkeypatch.setattr(schrodinger_sort.time, "sleep", lambda _: None)
    monkeypatch.setattr(schrodinger_sort.random, "choice", lambda seq: seq[0])
    monkeypatch.setattr(schrodinger_sort.random, "shuffle", lambda lst: lst.reverse())
    monkeypatch.setattr(schrodinger_sort.random, "random", lambda: 0.8)

    result, collapsed_to_sorted, _ = schrodinger_sort.schrodinger_sort(
        [4, 1, 3], meanness=0.0
    )

    assert collapsed_to_sorted is True
    assert result == [1, 3, 4]


def test_schrodinger_high_meanness_favors_unsorted(monkeypatch):
    monkeypatch.setattr(schrodinger_sort.time, "sleep", lambda _: None)
    monkeypatch.setattr(schrodinger_sort.random, "choice", lambda seq: seq[0])
    monkeypatch.setattr(schrodinger_sort.random, "shuffle", lambda lst: lst.reverse())
    monkeypatch.setattr(schrodinger_sort.random, "random", lambda: 0.8)

    result, collapsed_to_sorted, _ = schrodinger_sort.schrodinger_sort(
        [4, 1, 3], meanness=1.0
    )

    assert collapsed_to_sorted is False
    assert result != [1, 3, 4]


def test_schrodinger_rejects_out_of_range_meanness(monkeypatch):
    monkeypatch.setattr(schrodinger_sort.time, "sleep", lambda _: None)

    try:
        schrodinger_sort.schrodinger_sort([2, 1], meanness=1.1)
        assert False, "Expected ValueError for invalid meanness"
    except ValueError as exc:
        assert "meanness" in str(exc)


def test_urinal_sort_already_sorted_needs_no_rounds():
    result, rounds, logs, did_sort = urinal_sort.urinal_sort([1, 2, 3])

    assert did_sort is True
    assert rounds == 0
    assert result == [1, 2, 3]


def test_urinal_sort_sorts_in_one_round():
    # [1, 3, 2] with 3 stalls:
    #   1 → stall 0 (first in),  3 → stall 2,  2 → stall 1
    #   Reading: [1, 2, 3]  ✓
    result, rounds, logs, did_sort = urinal_sort.urinal_sort([1, 3, 2])

    assert did_sort is True
    assert result == [1, 2, 3]
    assert rounds == 1


def test_urinal_sort_detects_cycle():
    # [3, 2, 1]: round 1 → [3, 1, 2], round 2 → [3, 2, 1] — back to start.
    result, rounds, logs, did_sort = urinal_sort.urinal_sort([3, 2, 1], max_rounds=50)

    assert did_sort is False


def test_urinal_sort_rejects_out_of_range_awkwardness():
    with pytest.raises(ValidationError) as exc_info:
        urinal_sort.urinal_sort([2, 1], awkwardness=1.2)
    assert "awkwardness" in str(exc_info.value)


def test_digit_sort_sorts_correctly():
    sorted_nums, passes = digit_sort.digit_sort([170, 45, 75, 90, 2, 802, 66])

    assert sorted_nums == [2, 45, 66, 75, 90, 170, 802]


def test_digit_sort_returns_correct_number_of_passes():
    # max value 802 has 3 digits → 3 passes
    _, passes = digit_sort.digit_sort([170, 45, 75, 90, 2, 802, 66])

    assert len(passes) == 3


def test_digit_sort_single_element():
    sorted_nums, passes = digit_sort.digit_sort([7])

    assert sorted_nums == [7]
    assert len(passes) == 1


def test_digit_sort_already_sorted():
    sorted_nums, _ = digit_sort.digit_sort([1, 2, 3, 4, 5])

    assert sorted_nums == [1, 2, 3, 4, 5]


def test_digit_sort_reverse_order():
    sorted_nums, _ = digit_sort.digit_sort([9, 8, 7, 6, 5, 4, 3, 2, 1])

    assert sorted_nums == [1, 2, 3, 4, 5, 6, 7, 8, 9]


def test_digit_sort_with_duplicates():
    sorted_nums, _ = digit_sort.digit_sort([3, 1, 4, 1, 5, 9, 2, 6, 5])

    assert sorted_nums == [1, 1, 2, 3, 4, 5, 5, 6, 9]


def test_digit_sort_pass_buckets_contain_all_numbers():
    numbers = [170, 45, 75, 90, 2, 802, 66]
    _, passes = digit_sort.digit_sort(numbers)

    for pos, buckets, collected in passes:
        # All numbers must appear across all buckets combined each pass
        flat = [n for b in buckets for n in b]
        assert sorted(flat) == sorted(numbers)


def test_digit_sort_empty_list():
    sorted_nums, passes = digit_sort.digit_sort([])

    assert sorted_nums == []
    assert passes == []


def test_darwin_sort_returns_sorted_list(monkeypatch):
    # Patch time.sleep so the animation doesn't slow down the test suite.
    monkeypatch.setattr(darwin_sort.time, "sleep", lambda _: None)

    result, generations, elapsed, converged, logbook = darwin_sort.darwin_sort(
        [3, 1, 2], max_generations=1000
    )

    assert result == [1, 2, 3]
    assert converged is True
    assert generations >= 0
    assert len(logbook) > 0


def test_darwin_sort_single_element(monkeypatch):
    monkeypatch.setattr(darwin_sort.time, "sleep", lambda _: None)

    result, generations, elapsed, converged, logbook = darwin_sort.darwin_sort([7])

    assert result == [7]
    assert converged is True
    assert generations == 0


def test_darwin_sort_already_sorted(monkeypatch):
    monkeypatch.setattr(darwin_sort.time, "sleep", lambda _: None)

    result, generations, elapsed, converged, logbook = darwin_sort.darwin_sort(
        [1, 2, 3, 4, 5], max_generations=500
    )

    assert result == [1, 2, 3, 4, 5]
    assert converged is True


def test_darwin_sort_fitness_perfect_when_sorted():
    assert darwin_sort.fitness([1, 2, 3, 4, 5]) == (1.0,)


def test_darwin_sort_fitness_zero_when_reversed():
    assert darwin_sort.fitness([5, 4, 3, 2, 1]) == (0.0,)


def test_darwin_sort_fitness_partial():
    # [1, 3, 2, 4, 5] → 3 out of 4 pairs correct
    fit = darwin_sort.fitness([1, 3, 2, 4, 5])
    assert abs(fit[0] - 0.75) < 1e-9


def test_darwin_sort_best_returned_on_timeout(monkeypatch):
    monkeypatch.setattr(darwin_sort.time, "sleep", lambda _: None)

    # 10 elements → 10! = 3.6M permutations; probability of a 50-individual
    # population finding the sorted order in 1 generation is negligible (~0.001%).
    result, generations, elapsed, converged, logbook = darwin_sort.darwin_sort(
        [10, 9, 8, 7, 6, 5, 4, 3, 2, 1], max_generations=1
    )

    # Result must be a permutation of the input regardless of convergence.
    assert sorted(result) == list(range(1, 11))
    assert generations == 1
    assert converged is False


def test_darwin_sort_rejects_invalid_params(monkeypatch):
    monkeypatch.setattr(darwin_sort.time, "sleep", lambda _: None)

    with pytest.raises(ValidationError):
        darwin_sort.darwin_sort([3, 1, 2], population_size=0)

    with pytest.raises(ValidationError):
        darwin_sort.darwin_sort([3, 1, 2], crossover_prob=1.5)

    with pytest.raises(ValidationError):
        darwin_sort.darwin_sort([3, 1, 2], mutation_prob=-0.1)
