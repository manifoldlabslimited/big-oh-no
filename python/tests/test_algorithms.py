from big_oh_no import bogo_sort
from big_oh_no import linus_sort
from big_oh_no import schrodinger_sort
from big_oh_no import stalin_sort
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
