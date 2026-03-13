#!/usr/bin/env python3
"""
Shared utilities for Big O(No) sorting algorithms.
"""

from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, ValidationError
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich import box

console = Console()


def make_sort_header(icon: str, name: str, subtitle: str, style: str) -> Panel:
    """Build the standard spaced-out title panel used by every sort algorithm."""
    spaced = " ".join(name.upper())
    title = Text.assemble(
        (f"{icon} ", style),
        (spaced, f"bold {style}"),
        "   ",
        ("S O R T", "bold white"),
        (f" {icon}", style),
    )
    return Panel(
        Align.center(Text.assemble(title, "\n", Text(subtitle, style="dim italic"))),
        box=box.DOUBLE_EDGE,
        style=f"bold {style}",
        padding=(1, 2),
    )


class SortInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    numbers: list[Annotated[int, Field(strict=True)]] = Field(min_length=1)


__all__ = ["console", "make_sort_header", "SortInput", "ValidationError"]
