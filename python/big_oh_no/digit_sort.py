#!/usr/bin/env python3
"""
Digit Sort - A non-comparative sorting algorithm.
Inspired by Radix Sort: distributes numbers into digit buckets one position
at a time, from least-significant to most-significant digit.
No comparisons are ever made between numbers.
"""

import random
import time

from rich import box
from rich.align import Align
from rich.panel import Panel
from rich.rule import Rule
from rich.table import Table

from .utils import console, make_sort_header

FILING_REMARKS = [
    "Routed. No comparison was harmed in this process.",
    "Filed under the appropriate digit. Nothing personal.",
    "Deposited as directed by departmental policy.",
    "Allocated to correct bin — no judgement involved.",
    "Classified and shelved. The value is irrelevant to us.",
    "Stamped and filed. Next.",
    "Processed without prejudice.",
]

COLLECTION_REMARKS = [
    "Collecting buckets 0→9. No preferential treatment.",
    "Re-queuing from all buckets. The bureaucracy grinds on.",
    "Gathered and re-queued. Another pass awaits.",
    "All buckets emptied left to right. Order maintained.",
    "Collection complete. Deposited for next-pass processing.",
]

COMPLETION_REMARKS = [
    "Sorting complete. A comparison-free workplace was maintained throughout.",
    "Procedure concluded. Zero comparisons. The department is proud.",
    "Processing finished. Approved, stamped, and filed in triplicate.",
    "Workflow terminated normally. Zero comparisons. Maximum paperwork.",
]

ORDINALS = ["ones", "tens", "hundreds", "thousands", "ten-thousands"]


def create_header():
    return make_sort_header(
        "🗂️", "digit", "No comparisons. Just buckets and blind faith in process.", "blue"
    )


def create_stats_table(numbers):
    """Create input statistics table."""
    table = Table(
        title="📋 Intake Form",
        box=box.ROUNDED,
        title_style="bold yellow",
        show_header=True,
        header_style="bold cyan",
    )

    table.add_column("Field", style="dim")
    table.add_column("Value", style="green")

    max_val = max(numbers)
    num_digits = len(str(max_val))

    table.add_row("Batch", f"[bold]{numbers}[/bold]")
    table.add_row("Items", f"[cyan]{len(numbers)}[/cyan]")
    table.add_row("Passes required", f"[blue]{num_digits}[/blue]")
    table.add_row("Comparisons authorised", "[bold red]0[/bold red]")

    return table


def _get_digit(number, position):
    """Extract the digit at the given position (0 = ones, 1 = tens, ...)."""
    return (number // (10 ** position)) % 10


def _ordinal_label(pos):
    return ORDINALS[pos] if pos < len(ORDINALS) else f"10^{pos}"


def digit_sort(numbers):
    """
    Sort numbers using Digit Sort (LSD Radix Sort) with animated output.

    Distributes numbers into 10 buckets (0-9) based on the current digit
    position, from least-significant to most-significant.
    """
    if not numbers:
        return [], []

    nums = list(numbers)
    max_val = max(nums)
    num_digits = len(str(max_val))
    passes = []

    console.print()
    console.print(Align.center(create_stats_table(nums)))
    console.print()

    for pos in range(num_digits):
        label = _ordinal_label(pos)

        console.print(Rule(
            f"[bold blue]🗂️  Pass {pos + 1} — {label} digit[/bold blue]",
            style="blue",
        ))
        console.print()

        buckets = [[] for _ in range(10)]

        # Animate each number being filed into its bucket
        for n in nums:
            digit = _get_digit(n, pos)
            buckets[digit].append(n)
            remark = random.choice(FILING_REMARKS)
            console.print(
                f"  [cyan]{n:>5}[/cyan]  →  bucket [bold blue]{digit}[/bold blue]  "
                f"[dim italic]({remark})[/dim italic]"
            )
            time.sleep(0.25)

        console.print()

        # Show bucket summary
        console.print(_create_buckets_summary(buckets))

        # Collect from buckets
        collected = [n for bucket in buckets for n in bucket]
        passes.append((pos, [list(b) for b in buckets], list(collected)))
        nums = collected

        collection_remark = COLLECTION_REMARKS[pos] if pos < len(COLLECTION_REMARKS) else "Collecting and re-queuing."
        console.print(
            f"  [dim]→[/dim] [bold]{collected}[/bold]  "
            f"[dim italic]{collection_remark}[/dim italic]"
        )
        console.print()
        time.sleep(0.3)

    return nums, passes


def _create_buckets_summary(buckets):
    """Compact bucket summary showing only non-empty buckets."""
    table = Table(
        box=box.SIMPLE_HEAVY,
        show_header=True,
        header_style="bold blue",
        padding=(0, 1),
    )

    table.add_column("Bucket", style="bold cyan", justify="center", width=8)
    table.add_column("Contents", style="green")
    table.add_column("#", style="magenta", justify="center", width=5)

    for digit, bucket in enumerate(buckets):
        if bucket:
            contents = ", ".join(str(n) for n in bucket)
            table.add_row(str(digit), f"[bold]{contents}[/bold]", str(len(bucket)))

    return Align.center(table)


def create_result_table(original, sorted_nums, passes):
    """Create a summary table after all passes."""
    table = Table(
        title="📁 Filing Report",
        box=box.ROUNDED,
        title_style="bold green",
        show_header=True,
        header_style="bold cyan",
    )

    table.add_column("Stage", style="dim")
    table.add_column("Sequence", style="cyan")

    table.add_row("Submitted", f"{original}")
    for pos, _buckets, collected in passes:
        table.add_row(f"After {_ordinal_label(pos)} pass", f"[bold]{collected}[/bold]")
    table.add_row("[bold green]Filed & approved[/bold green]", f"[bold green]{sorted_nums}[/bold green]")

    return table


def create_comparison_bars(original, sorted_nums):
    """Visual bar comparison of before and after."""
    max_val = max(max(original), max(sorted_nums)) if original else 1
    bar_scale = 25 / max_val

    console.print("\n[bold yellow]📋 Before:[/bold yellow]")
    for num in original:
        bar = "█" * int(num * bar_scale)
        console.print(f"  [dim]{num:>5}[/dim] │[magenta]{bar}[/magenta]")

    console.print("\n[bold green]✅ After:[/bold green]")
    for num in sorted_nums:
        bar = "█" * int(num * bar_scale)
        console.print(f"  [dim]{num:>5}[/dim] │[green]{bar}[/green]")
