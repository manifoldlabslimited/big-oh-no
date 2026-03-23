"""Tests for the visualization framework and algorithm viz generators."""

import pytest
from unittest.mock import patch, MagicMock

from big_oh_no.visualizer import Action, VizFrame, run_visualization


# ── VizFrame / Action basics ─────────────────────────────────────────────────

def test_vizframe_defaults():
    frame = VizFrame(bars=[1, 2, 3])
    assert frame.highlighted == []
    assert frame.action == Action.COMPARE
    assert frame.label == ""
    assert frame.log_line == ""


def test_action_enum_values():
    assert Action.ELIMINATE.value == "eliminate"
    assert Action.DONE.value == "done"
    assert Action.SHUFFLE.value == "shuffle"
    assert Action.EVOLVE.value == "evolve"


# ── run_visualization ─────────────────────────────────────────────────────────

def test_run_visualization_returns_final_bars():
    frames = iter([
        VizFrame(bars=[3, 1, 2], highlighted=[0], action=Action.COMPARE, label="cmp"),
        VizFrame(bars=[1, 2, 3], highlighted=[0, 1, 2], action=Action.DONE, label="done"),
    ])
    result = run_visualization(frames, algo_name="Test", delay=0, sound=False)
    assert result == [1, 2, 3]


def test_run_visualization_empty_frames():
    result = run_visualization(iter([]), algo_name="Test", delay=0, sound=False)
    assert result == []


def test_run_visualization_single_frame():
    frames = iter([
        VizFrame(bars=[5], highlighted=[0], action=Action.DONE, label="done"),
    ])
    result = run_visualization(frames, algo_name="Test", delay=0, sound=False)
    assert result == [5]


def test_run_visualization_collects_log_lines():
    """Log lines don't affect the return value — just verifying no crash."""
    frames = iter([
        VizFrame(bars=[2, 1], highlighted=[], action=Action.COMPARE, log_line="[dim]start[/dim]"),
        VizFrame(bars=[1, 2], highlighted=[0, 1], action=Action.DONE, log_line="[green]done[/green]"),
    ])
    result = run_visualization(frames, algo_name="Test", delay=0, sound=False)
    assert result == [1, 2]


# ── Stalin Sort viz generator ─────────────────────────────────────────────────

def test_stalin_sort_viz_produces_correct_result():
    from big_oh_no.stalin_sort import stalin_sort_viz

    result = {}
    frames = list(stalin_sort_viz([5, 1, 9, 2, 8], result=result))

    assert result["survivors"] == [5, 9]
    assert result["eliminated"] == [1, 2, 8]

    # Last frame should be DONE
    assert frames[-1].action == Action.DONE
    assert frames[-1].bars == [5, 9]


def test_stalin_sort_viz_all_survive():
    from big_oh_no.stalin_sort import stalin_sort_viz

    result = {}
    frames = list(stalin_sort_viz([1, 2, 3], result=result))

    assert result["survivors"] == [1, 2, 3]
    assert result["eliminated"] == []
    assert frames[-1].action == Action.DONE


def test_stalin_sort_viz_without_result_dict():
    from big_oh_no.stalin_sort import stalin_sort_viz

    frames = list(stalin_sort_viz([3, 1, 2]))
    assert frames[-1].action == Action.DONE


def test_stalin_sort_viz_has_eliminate_frames():
    from big_oh_no.stalin_sort import stalin_sort_viz

    frames = list(stalin_sort_viz([5, 1, 9]))
    eliminate_frames = [f for f in frames if f.action == Action.ELIMINATE]
    assert len(eliminate_frames) == 1  # only 1 is eliminated


# ── Darwin Sort viz generator ─────────────────────────────────────────────────

def test_darwin_sort_viz_produces_correct_result():
    from big_oh_no.darwin_sort import darwin_sort_viz

    result = {}
    frames = list(darwin_sort_viz([3, 1, 2], max_generations=500, result=result))

    assert result["sorted"] == [1, 2, 3]
    assert result["converged"] is True
    assert frames[-1].action == Action.DONE


def test_darwin_sort_viz_single_element():
    from big_oh_no.darwin_sort import darwin_sort_viz

    result = {}
    frames = list(darwin_sort_viz([7], result=result))

    assert result["sorted"] == [7]
    assert result["converged"] is True
    assert len(frames) == 1
    assert frames[0].action == Action.DONE


def test_darwin_sort_viz_without_result_dict():
    from big_oh_no.darwin_sort import darwin_sort_viz

    frames = list(darwin_sort_viz([2, 1], max_generations=500))
    assert frames[-1].action == Action.DONE


def test_darwin_sort_viz_extinction():
    from big_oh_no.darwin_sort import darwin_sort_viz

    result = {}
    frames = list(darwin_sort_viz(
        [10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
        max_generations=1,
        population_size=2,
        result=result,
    ))

    # With only 1 generation and 2 individuals, convergence is near-impossible
    assert frames[-1].action == Action.DONE
    assert "sorted" in result


def test_darwin_sort_viz_rejects_invalid_params():
    from big_oh_no.darwin_sort import darwin_sort_viz
    from pydantic import ValidationError

    with pytest.raises(ValidationError):
        list(darwin_sort_viz([3, 1, 2], crossover_prob=0.8, mutation_prob=0.5))
