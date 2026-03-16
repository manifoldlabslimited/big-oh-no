#!/usr/bin/env python3
"""
Digit Sort - A non-comparative sorting algorithm.
Inspired by Radix Sort: distributes numbers into digit buckets one position
at a time, from least-significant to most-significant digit.
No comparisons are ever made between numbers.
"""

import time

from rich import box
from rich.align import Align
from rich.panel import Panel
from rich.rule import Rule
from rich.table import Table

from .utils import console, make_sort_header

FRAME_DELAY = 0.05


def create_header():
    return make_sort_header("🔢", "digit", "No comparisons needed — just buckets all the way down", "blue")


def create_stats_table(numbers):
    """Create input statistics table."""
    if not numbers:
        return Table(title="📦 Sort Configuration", box=box.ROUNDED)

    table = Table(
        title="📦 Sort Configuration",
        box=box.ROUNDED,
        title_style="bold yellow",
        show_header=True,
        header_style="bold cyan",
    )

    table.add_column("Property", style="dim")
    table.add_column("Value", style="green")

    max_val = max(numbers)
    num_digits = len(str(max_val))

    table.add_row("Numbers to sort", f"[bold]{numbers}[/bold]")
    table.add_row("Count", f"[cyan]{len(numbers)}[/cyan] elements")
    table.add_row("Maximum value", f"[magenta]{max_val}[/magenta]")
    table.add_row("Digit passes required", f"[blue]{num_digits}[/blue]")

    return table


def _get_digit(number, position):
    """Extract the digit at the given position (0 = ones, 1 = tens, ...)."""
    return (number // (10 ** position)) % 10


def digit_sort(numbers):
    """
    Sort numbers using Digit Sort (LSD Radix Sort).

    Distributes numbers into 10 buckets (0–9) based on the current digit
    position, from least-significant to most-significant, collecting and
    repeating until all digit positions are processed.

    Returns:
        sorted_nums: the fully sorted list
        passes: list of (digit_position, buckets_snapshot, collected_order)
                one entry per digit-position pass
    """
    if not numbers:
        return [], []

    nums = list(numbers)
    max_val = max(nums)
    num_digits = len(str(max_val))
    passes = []

    for pos in range(num_digits):
        buckets = [[] for _ in range(10)]
        for n in nums:
            digit = _get_digit(n, pos)
            buckets[digit].append(n)

        collected = [n for bucket in buckets for n in bucket]
        passes.append((pos, [list(b) for b in buckets], list(collected)))
        nums = collected

    return nums, passes


def create_buckets_table(pos, buckets, collected):
    """Render a pass's bucket distribution as a Rich table."""
    ordinal = ["ones", "tens", "hundreds", "thousands", "ten-thousands"]
    label = ordinal[pos] if pos < len(ordinal) else f"10^{pos}"

    table = Table(
        title=f"Pass {pos + 1} — [bold cyan]{label}[/bold cyan] digit",
        box=box.ROUNDED,
        title_style="bold yellow",
        show_header=True,
        header_style="bold blue",
    )

    table.add_column("Bucket", style="bold cyan", justify="center", width=8)
    table.add_column("Contents", style="green")
    table.add_column("Count", style="magenta", justify="center", width=7)

    for digit, bucket in enumerate(buckets):
        if bucket:
            contents = "  ".join(f"[bold]{n}[/bold]" for n in bucket)
            table.add_row(f"[bold]{digit}[/bold]", contents, str(len(bucket)))
        else:
            table.add_row(f"[dim]{digit}[/dim]", "[dim]—[/dim]", "[dim]0[/dim]")

    return table


def create_result_table(original, sorted_nums, passes):
    """Create a summary table after all passes."""
    table = Table(
        title="🏆 Sort Summary",
        box=box.ROUNDED,
        title_style="bold green",
        show_header=True,
        header_style="bold cyan",
    )

    table.add_column("Stage", style="dim")
    table.add_column("Numbers", style="cyan")

    table.add_row("[dim]Original[/dim]", f"{original}")
    for pos, buckets, collected in passes:
        ordinal = ["ones", "tens", "hundreds", "thousands", "ten-thousands"]
        label = ordinal[pos] if pos < len(ordinal) else f"10^{pos}"
        table.add_row(f"After {label} pass", f"[bold]{collected}[/bold]")

    table.add_row("[bold green]Sorted[/bold green]", f"[bold green]{sorted_nums}[/bold green]")

    return table
