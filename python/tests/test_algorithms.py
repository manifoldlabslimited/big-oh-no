import linus_sort
import stalin_sort
import wait_sort


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
