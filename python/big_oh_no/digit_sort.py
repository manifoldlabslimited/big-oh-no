#!/usr/bin/env python3
"""
Digit Sort - A non-comparative sorting algorithm.
Inspired by Radix Sort: distributes numbers into digit buckets one position
at a time, from least-significant to most-significant digit.
No comparisons are ever made between numbers.
"""

from rich import box
from rich.align import Align
from rich.panel import Panel
from rich.rule import Rule
from rich.table import Table

from .utils import console, make_sort_header

# Bureaucratic filing commentary, one per pass
PASS_OPENING_REMARKS = [
    "Examining the ones column. All forms routed by least-significant digit — as per Form 7G.",
    "Proceeding to the tens column. Please hold your enquiries until all buckets are full.",
    "Hundreds column now under review. The department thanks you for your patience.",
    "Thousands digit processing initiated. Kindly refrain from comparing values at this time.",
    "Ten-thousands column. We are aware this is taking longer than expected. This is normal.",
]

BUCKET_ASSIGNMENT_FLAVOUR = [
    "Routed. No comparison was harmed in this process.",
    "Filed correctly under the appropriate digit. Nothing personal.",
    "Deposited into bucket as directed by departmental policy.",
    "Allocated to correct bin — no individual judgement involved.",
    "Classified and shelved. The value of this number is irrelevant to us.",
]

COLLECTION_REMARKS = [
    "Collecting buckets 0 through 9 in strict order. No preferential treatment.",
    "Re-queuing forms from all buckets. The bucket number, not the contents, governs order.",
    "Gathered and re-queued. Another pass awaits, if regulations require it.",
    "All buckets emptied left to right. The bureaucracy grinds on.",
    "Collection complete. Deposited into the outbox for next-pass processing.",
]

COMPLETION_REMARKS = [
    "All forms filed correctly. Sorting complete. A comparison-free workplace was maintained throughout.",
    "Procedure concluded. No numbers were compared. The department is proud of its restraint.",
    "Processing finished. The sorted list has been approved, stamped, and filed in triplicate.",
    "Workflow terminated normally. Zero comparisons. Maximum paperwork. Perfect outcome.",
]


def create_header():
    return make_sort_header(
        "🗂️", "digit", "No comparisons ever. Just buckets, bureaucracy, and blind faith in process.", "blue"
    )


def create_stats_table(numbers):
    """Create input statistics table."""
    if not numbers:
        return Table(title="📋 Intake Form", box=box.ROUNDED)

    table = Table(
        title="📋 Intake Form — Please Read Before Processing",
        box=box.ROUNDED,
        title_style="bold yellow",
        show_header=True,
        header_style="bold cyan",
    )

    table.add_column("Field", style="dim")
    table.add_column("Value", style="green")

    max_val = max(numbers)
    num_digits = len(str(max_val))

    table.add_row("Batch submitted for filing", f"[bold]{numbers}[/bold]")
    table.add_row("Number of items in batch", f"[cyan]{len(numbers)}[/cyan]")
    table.add_row("Largest value on record", f"[magenta]{max_val}[/magenta]")
    table.add_row("Passes required (digits)", f"[blue]{num_digits}[/blue]")
    table.add_row("Comparisons authorised", "[bold red]0[/bold red]")

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


def create_buckets_table(pos, buckets):
    """Render a pass's bucket distribution as a Rich table."""
    ordinal = ["ones", "tens", "hundreds", "thousands", "ten-thousands"]
    label = ordinal[pos] if pos < len(ordinal) else f"10^{pos}"
    remark = PASS_OPENING_REMARKS[pos] if pos < len(PASS_OPENING_REMARKS) else "Processing next digit column."

    table = Table(
        title=f"🗂️  Pass {pos + 1} — [bold cyan]{label}[/bold cyan] digit\n"
              f"[dim italic]{remark}[/dim italic]",
        box=box.ROUNDED,
        title_style="bold yellow",
        show_header=True,
        header_style="bold blue",
    )

    table.add_column("Bucket", style="bold cyan", justify="center", width=8)
    table.add_column("Filed Items", style="green")
    table.add_column("Count", style="magenta", justify="center", width=7)
    table.add_column("Status", style="dim", width=14)

    for digit, bucket in enumerate(buckets):
        if bucket:
            contents = "  ".join(f"[bold]{n}[/bold]" for n in bucket)
            table.add_row(
                f"[bold]{digit}[/bold]",
                contents,
                str(len(bucket)),
                "[green]Filed ✓[/green]",
            )
        else:
            table.add_row(
                f"[dim]{digit}[/dim]",
                "[dim]— empty —[/dim]",
                "[dim]0[/dim]",
                "[dim]No submissions[/dim]",
            )

    return table


def create_result_table(original, sorted_nums, passes):
    """Create a summary table after all passes."""
    table = Table(
        title="📁 Final Filing Report",
        box=box.ROUNDED,
        title_style="bold green",
        show_header=True,
        header_style="bold cyan",
    )

    table.add_column("Stage", style="dim")
    table.add_column("Output Sequence", style="cyan")

    table.add_row("[dim]Submitted batch[/dim]", f"{original}")
    for pos, buckets, collected in passes:
        ordinal = ["ones", "tens", "hundreds", "thousands", "ten-thousands"]
        label = ordinal[pos] if pos < len(ordinal) else f"10^{pos}"
        table.add_row(f"After {label} pass", f"[bold]{collected}[/bold]")

    table.add_row("[bold green]Approved & filed[/bold green]", f"[bold green]{sorted_nums}[/bold green]")

    return table
