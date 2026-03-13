#!/usr/bin/env python3
"""
Schrödinger Sort — The list is simultaneously sorted and unsorted until you
observe it, at which point it collapses into whichever state is least
convenient.
"""

import random
import time

from rich import box
from rich.align import Align
from rich.panel import Panel
from rich.rule import Rule
from rich.table import Table

from .utils import console, make_sort_header


COLLAPSE_COMMENTS_SORTED = [
    "The universe was annoyingly helpful. You're welcome.",
    "Against all odds, order prevailed. Don't get used to it.",
    "Quantum mechanics decided to cooperate today. Suspicious.",
    "The wavefunction collapsed into your desired state. This won't happen twice.",
    "Sorted. The cat lives. This time.",
]

COLLAPSE_COMMENTS_UNSORTED = [
    "The universe maintained its commitment to chaos. As expected.",
    "Order was never really an option, was it.",
    "The wavefunction chose entropy. Obviously.",
    "The cat is probably fine. The list is not.",
    "You looked at it wrong. Now it's unsorted.",
]


def create_header():
    return make_sort_header("🐱", "schrodinger", "Sorted and unsorted, until you look", "blue")


def create_stats_table(numbers):
    table = Table(
        title="⚛️  Quantum Input Analysis",
        box=box.ROUNDED,
        title_style="bold cyan",
        show_header=True,
        header_style="bold blue",
    )
    table.add_column("Property", style="dim")
    table.add_column("Value", style="cyan")

    table.add_row("Numbers to sort", f"[bold]{numbers}[/bold]")
    table.add_row("Count", f"[cyan]{len(numbers)}[/cyan] elements")
    table.add_row("Current state", "[yellow]⚛️  superposition[/yellow]")
    table.add_row("Observer", "[red]YOU (dangerous)[/red]")

    return table


def create_superposition_table(sorted_state, unsorted_state):
    table = Table(
        title="⚛️  Quantum Superposition",
        box=box.ROUNDED,
        title_style="bold cyan",
        show_header=True,
        header_style="bold",
    )
    table.add_column("Eigenstate", min_width=18)
    table.add_column("Values", style="bold")
    table.add_column("Amplitude", justify="center")

    table.add_row(
        "[green]|sorted⟩[/green]",
        f"[green]{sorted_state}[/green]",
        "[green]1/√2[/green]",
    )
    table.add_row(
        "[magenta]|unsorted⟩[/magenta]",
        f"[magenta]{unsorted_state}[/magenta]",
        "[magenta]1/√2[/magenta]",
    )
    table.add_row(
        "[dim]|observed⟩[/dim]",
        "[dim]???[/dim]",
        "[yellow]pending ⚠️[/yellow]",
    )

    return table


def is_sorted(values):
    return all(values[i] <= values[i + 1] for i in range(len(values) - 1))


def schrodinger_sort(numbers, _collapse=None):
    """
    Observe the list, collapsing it into its least convenient state.

    _collapse: optional bool to force the outcome (for testing).
               True → sorted, False → unsorted.

    Returns (result, collapsed_to_sorted, comment)
    """
    candidate = numbers.copy()
    sorted_state = sorted(candidate)
    unsorted_state = candidate.copy()
    random.shuffle(unsorted_state)

    already_sorted = candidate == sorted_state

    console.print()
    console.print(create_header())
    console.print()
    console.print(Align.center(create_stats_table(candidate)))
    console.print()
    console.print(Align.center(create_superposition_table(sorted_state, unsorted_state)))
    console.print()

    console.print(Rule("[bold cyan]🔬 Initiating Quantum Observation[/bold cyan]", style="cyan"))
    console.print()
    if already_sorted:
        console.print(
            "[dim]  Note: the input is already sorted. "
            "The universe has taken note of your hubris.[/dim]"
        )
    else:
        console.print("[dim]  Warning: observing this list will collapse its quantum state.[/dim]")
    console.print("[dim]  The universe will select the least convenient outcome.[/dim]")
    console.print()

    steps = [
        "🔬 Warming up quantum measurement apparatus...",
        "⚛️  Entangling adjacent elements...",
        "🌀 Superimposing sorted and unsorted eigenstates...",
        "📡 Detecting observer presence...",
        "👀 Observer confirmed. Preparing to collapse wavefunction...",
    ]
    for step in steps:
        time.sleep(0.5)
        console.print(f"  [dim cyan]{step}[/dim cyan]")

    time.sleep(0.6)
    console.print()

    # Determine collapse outcome
    if _collapse is not None:
        collapsed_to_sorted = _collapse
    elif already_sorted:
        # Already sorted → the universe gleefully destroys it
        collapsed_to_sorted = False
    else:
        collapsed_to_sorted = random.random() < 0.5

    result = sorted_state if collapsed_to_sorted else unsorted_state
    comment = random.choice(
        COLLAPSE_COMMENTS_SORTED if collapsed_to_sorted else COLLAPSE_COMMENTS_UNSORTED
    )

    if collapsed_to_sorted:
        console.print(Rule(
            "[bold green]✨ Wavefunction collapsed → |sorted⟩[/bold green]",
            style="green",
        ))
    else:
        console.print(Rule(
            "[bold magenta]💥 Wavefunction collapsed → |unsorted⟩[/bold magenta]",
            style="magenta",
        ))

    console.print()
    console.print(f"  [dim italic]\"{comment}\"[/dim italic]")
    console.print()

    return result, collapsed_to_sorted, comment


def create_result_table(original, result, collapsed_to_sorted, comment):
    table = Table(
        title="📊 Collapse Report",
        box=box.ROUNDED,
        title_style="bold yellow",
        show_header=True,
        header_style="bold cyan",
    )
    table.add_column("Property", style="dim")
    table.add_column("Value", style="cyan")

    col = "green" if collapsed_to_sorted else "magenta"
    label = "sorted ✨" if collapsed_to_sorted else "unsorted 💥"

    table.add_row("Original", f"{original}")
    table.add_row("Result", f"[bold]{result}[/bold]")
    table.add_row("Collapsed to", f"[{col}]{label}[/{col}]")
    table.add_row("Universe's verdict", f"[dim italic]{comment}[/dim italic]")

    return table


def create_result_panel(original, result, collapsed_to_sorted, comment):
    if collapsed_to_sorted:
        message = (
            "[bold green]The wavefunction chose order.[/bold green]\n\n"
            f"[dim]Original:[/dim] {original}\n"
            f"[dim]Result:[/dim]   [bold cyan]{result}[/bold cyan]\n\n"
            f"[dim italic]\"{comment}\"[/dim italic]"
        )
        title = "[bold yellow]✨ Collapsed → Sorted[/bold yellow]"
        style = "green"
    else:
        message = (
            "[bold magenta]The wavefunction chose entropy.[/bold magenta]\n\n"
            f"[dim]Original:[/dim] {original}\n"
            f"[dim]Result:[/dim]   [bold cyan]{result}[/bold cyan]\n\n"
            f"[dim italic]\"{comment}\"[/dim italic]"
        )
        title = "[bold yellow]💥 Collapsed → Unsorted[/bold yellow]"
        style = "magenta"

    return Panel(message, title=title, box=box.DOUBLE, style=style)
