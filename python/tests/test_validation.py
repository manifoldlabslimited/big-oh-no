import click
import pytest

from cli import parse_numbers, parse_wait_input


def test_parse_numbers_valid():
    assert parse_numbers((5, 1, 9)) == [5, 1, 9]


def test_parse_numbers_rejects_empty():
    with pytest.raises(click.BadParameter):
        parse_numbers(())


def test_parse_wait_input_valid():
    numbers, scale = parse_wait_input((5, 2, 1), 0.25)
    assert numbers == [5, 2, 1]
    assert scale == 0.25


def test_parse_wait_input_rejects_non_positive_scale():
    with pytest.raises(click.BadParameter):
        parse_wait_input((5, 2, 1), 0)
