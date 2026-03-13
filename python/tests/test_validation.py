import click
import pytest

from cli import parse_numbers


def test_parse_numbers_valid():
    assert parse_numbers((5, 1, 9)) == [5, 1, 9]


def test_parse_numbers_rejects_empty():
    with pytest.raises(click.BadParameter):
        parse_numbers(())
