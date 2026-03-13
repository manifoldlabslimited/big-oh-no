#!/usr/bin/env python3
"""
Bogo Sort - A sorting algorithm powered by blind optimism.
It keeps shuffling until the list is sorted (or luck runs out).
"""

import random
import time

from rich import box
from rich.align import Align
from rich.panel import Panel
from rich.progress import BarColumn
from rich.progress import Progress
from rich.progress import SpinnerColumn
from rich.progress import TextColumn
from rich.rule import Rule
from rich.table import Table

from .utils import console, make_sort_header

FRAME_DELAY = 0.002


def create_header():
    return make_sort_header("🎲", "bogo", "Randomness is a strategy (technically)", "magenta")


def create_stats_table(numbers, max_attempts):
    """Create a stats table for the input."""
    table = Table(
        title="🎰 Chaos Configuration",
        box=box.ROUNDED,
        title_style="bold yellow",
        show_header=True,
        header_style="bold cyan",
    )

    table.add_column("Property", style="dim")
    table.add_column("Value", style="green")

    table.add_row("Numbers to sort", f"[bold]{numbers}[/bold]")
    table.add_row("Count", f"[cyan]{len(numbers)}[/cyan] elements")
    table.add_row("Max attempts", f"[magenta]{max_attempts}[/magenta]")

    return table


def is_sorted(values):
    """Return True when values are monotonic non-decreasing."""
    return all(values[i] <= values[i + 1] for i in range(len(values) - 1))


def order_score(values):
    """Count adjacent pairs that are already in non-decreasing order."""
    return sum(1 for i in range(len(values) - 1) if values[i] <= values[i + 1])


def bogo_sort(numbers, max_attempts=10000):
    """Sort by repeatedly shuffling until order appears."""
    candidate = numbers.copy()
    attempts = 0
    started = time.time()
    max_score = max(len(numbers) - 1, 0)
    best_score = order_score(candidate)
    best_candidate = candidate.copy()

    hype_lines = [
        "[yellow]🎲 Dealer says: trust the chaos[/yellow]",
        "[yellow]🎲 Probability is just confidence wearing math[/yellow]",
        "[yellow]🎲 One more shuffle surely fixes everything[/yellow]",
        "[yellow]🎲 This is definitely a strategy[/yellow]",
    ]

    console.print()
    console.print(create_header())
    console.print()
    console.print(Align.center(create_stats_table(candidate, max_attempts)))
    console.print()
    console.print(Rule("[bold magenta]🎲 Entering Random Shuffle Loop[/bold magenta]", style="magenta"))

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=40, style="magenta", complete_style="green", finished_style="green"),
        TextColumn("[cyan]{task.completed}[/cyan]/[dim]{task.total}[/dim] attempts"),
        console=console,
        expand=False,
    ) as progress:
        task_id = progress.add_task(
            "[yellow]🎲 Shuffling permutations...[/yellow]",
            total=max_attempts,
        )

        while not is_sorted(candidate) and attempts < max_attempts:
            random.shuffle(candidate)
            attempts += 1
            score = order_score(candidate)

            # Keep animation perceptible without turning each run into a long wait.
            if attempts <= 120 or attempts % 250 == 0:
                time.sleep(FRAME_DELAY)

            if score > best_score:
                best_score = score
                best_candidate = candidate.copy()

            if attempts <= 20 or attempts % 100 == 0 or score == max_score:
                meter = f"[magenta]{score}/{max_score} ordered pairs[/magenta]"
                hype = hype_lines[attempts % len(hype_lines)]
                progress.update(
                    task_id,
                    completed=attempts,
                    description=(
                        f"[yellow]🎲 Try {attempts}:[/yellow] [bold]{candidate}[/bold] "
                        f"[dim]({meter})[/dim] {hype}"
                    ),
                )
            else:
                progress.update(task_id, completed=attempts)

        if is_sorted(candidate):
            final_desc = "[green]✅ Jackpot: sorted permutation found[/green]"
        else:
            final_desc = (
                "[yellow]⚠️ Max attempts reached[/yellow] "
                f"[dim](best near-miss: {best_candidate}, {best_score}/{max_score} ordered pairs)[/dim]"
            )
        progress.update(task_id, completed=attempts, description=final_desc)

    elapsed = time.time() - started

    console.print()
    if is_sorted(candidate):
        console.print(Rule("[bold green]✨ Statistical Miracle Achieved[/bold green]", style="green"))
    else:
        console.print(Rule("[bold yellow]⚠️ Luck Budget Exhausted[/bold yellow]", style="yellow"))

    return candidate, attempts, elapsed


def create_result_table(original, sorted_candidate, attempts, elapsed):
    """Create result table for bogo sort."""
    table = Table(
        title="📊 Bogo Sort Report",
        box=box.ROUNDED,
        title_style="bold yellow",
        show_header=True,
        header_style="bold cyan",
    )

    table.add_column("Property", style="dim")
    table.add_column("Value", style="cyan")

    table.add_row("Original", f"{original}")
    table.add_row("Current", f"[bold]{sorted_candidate}[/bold]")
    table.add_row("Shuffles", f"[magenta]{attempts}[/magenta]")
    table.add_row("Elapsed", f"[green]{elapsed:.4f}s[/green]")
    table.add_row(
        "Order meter",
        f"[yellow]{order_score(sorted_candidate)}/{max(len(sorted_candidate) - 1, 0)}[/yellow] adjacent pairs in order",
    )
    table.add_row("Sorted?", "[green]Yes[/green]" if is_sorted(sorted_candidate) else "[red]No[/red]")

    return table


def create_result_panel(original, sorted_candidate, attempts, elapsed):
    """Create summary panel for CLI output."""
    if is_sorted(sorted_candidate):
        message = (
            "[bold green]Order emerged from pure chaos.[/bold green]\n\n"
            f"[dim]Original:[/dim] {original}\n"
            f"[dim]Sorted:[/dim]   [bold cyan]{sorted_candidate}[/bold cyan]\n"
            f"[dim]Shuffles:[/dim] {attempts}\n"
            f"[dim]Time:[/dim]     {elapsed:.4f}s"
        )
        title = "[bold yellow]🎉 Bogo Success[/bold yellow]"
        style = "green"
    else:
        message = (
            "[bold yellow]No sorted permutation was discovered in time.[/bold yellow]\n\n"
            f"[dim]Original:[/dim] {original}\n"
            f"[dim]Current:[/dim]  [bold cyan]{sorted_candidate}[/bold cyan]\n"
            f"[dim]Shuffles:[/dim] {attempts}\n"
            f"[dim]Time:[/dim]     {elapsed:.4f}s"
        )
        title = "[bold yellow]🎲 Bogo Timeout[/bold yellow]"
        style = "yellow"

    return Panel(message, title=title, box=box.DOUBLE, style=style)
