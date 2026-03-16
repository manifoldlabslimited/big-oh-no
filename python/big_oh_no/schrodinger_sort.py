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

QUANTUM_STATES = [
    "⚛️  superposition",
    "🌀 entangled",
    "✨ coherent",
    "💫 tunnelling",
    "🔮 uncertain",
    "🌊 wave-like",
    "⚡ excited",
]

OBSERVATION_REMARKS = [
    "Heisenberg would not approve of this.",
    "The particle noticed you looking.",
    "Uncertainty principle: engaged.",
    "This measurement changed the outcome.",
    "The act of reading this altered the result.",
    "Schrödinger's cat just hissed at you.",
    "Quantum decoherence in progress...",
    "The eigenvalue is judging you.",
]


def create_header():
    return make_sort_header("🐱", "schrodinger", "Sorted and unsorted, until you look", "blue")


def create_stats_table(numbers, meanness):
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
    table.add_row("Meanness", f"[magenta]{meanness:.2f}[/magenta]")
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


def order_score(values):
    """Count adjacent pairs that are already in non-decreasing order."""
    return sum(1 for i in range(len(values) - 1) if values[i] <= values[i + 1])


def collapse_probability(values, meanness):
    """Return probability of collapsing into sorted state."""
    hostility = meanness

    max_pairs = max(len(values) - 1, 1)
    order_ratio = order_score(values) / max_pairs
    p_sorted = (1.0 - hostility) - (0.4 * order_ratio) + 0.2
    return max(0.05, min(0.95, p_sorted))


def _probability_bar(p_sorted):
    """Render a visual probability meter."""
    width = 20
    filled_green = int(width * p_sorted)
    filled_magenta = width - filled_green
    bar = f"[green]{'█' * filled_green}[/green][magenta]{'█' * filled_magenta}[/magenta]"
    return f"|sorted⟩ {bar} |unsorted⟩  ({p_sorted:.0%} / {1 - p_sorted:.0%})"


def schrodinger_sort(numbers, meanness=0.5, _collapse=None):
    """
    Observe the list, collapsing it into its least convenient state.

    _collapse: optional bool to force the outcome (for testing).
               True → sorted, False → unsorted.

    meanness: 0.0-1.0 dial. Higher means less chance of sorted collapse.

    Returns (result, collapsed_to_sorted, comment)
    """
    if not 0.0 <= meanness <= 1.0:
        raise ValueError("meanness must be between 0.0 and 1.0")

    candidate = numbers.copy()
    sorted_state = sorted(candidate)
    unsorted_state = candidate.copy()
    random.shuffle(unsorted_state)

    already_sorted = candidate == sorted_state

    console.print()
    console.print(create_header())
    console.print()
    console.print(Align.center(create_stats_table(candidate, meanness)))
    console.print()
    console.print(Align.center(create_superposition_table(sorted_state, unsorted_state)))
    console.print()

    # --- Phase 1: Per-element quantum state assignment ---
    console.print(Rule("[bold cyan]🔬 Quantum State Preparation[/bold cyan]", style="cyan"))
    console.print()

    if already_sorted:
        console.print(
            "  [dim]Note: the input is already sorted. "
            "The universe has taken note of your hubris.[/dim]"
        )
    else:
        console.print("  [dim]Each element enters superposition as it is observed...[/dim]")
    console.print()

    for num in candidate:
        state = random.choice(QUANTUM_STATES)
        time.sleep(0.35)
        console.print(
            f"  [bold cyan]{num:>5}[/bold cyan]  →  [yellow]{state}[/yellow]  "
            f"[dim italic]({random.choice(OBSERVATION_REMARKS)})[/dim italic]"
        )

    console.print()
    time.sleep(0.3)

    # --- Phase 2: Apparatus warm-up ---
    console.print(Rule("[bold cyan]⚛️  Measurement Apparatus[/bold cyan]", style="cyan"))
    console.print()

    steps = [
        "🔬 Calibrating quantum measurement apparatus...",
        "⚛️  Entangling adjacent elements...",
        "🌀 Superimposing sorted and unsorted eigenstates...",
        "📡 Detecting observer presence...",
        "👀 Observer confirmed. Wavefunction destabilising...",
    ]
    for step in steps:
        time.sleep(0.4)
        console.print(f"  [dim cyan]{step}[/dim cyan]")

    console.print()
    time.sleep(0.3)

    # --- Phase 3: Probability meter ---
    p_sorted = collapse_probability(candidate, meanness)
    console.print(
        f"  [dim]Meanness dial:[/dim] [magenta]{meanness:.2f}[/magenta]  →  "
        f"[dim]p(sorted) ≈[/dim] [cyan]{p_sorted:.2f}[/cyan]"
    )
    console.print(f"  {_probability_bar(p_sorted)}")
    console.print()

    # --- Phase 4: Dramatic collapse countdown ---
    console.print(Rule("[bold yellow]⚠️  Wavefunction Collapse Imminent[/bold yellow]", style="yellow"))
    console.print()

    cat_frames = ["🐱", "🙀", "😿", "😾", "🐱"]
    for i, frame in enumerate(cat_frames):
        time.sleep(0.4)
        dots = "." * (i + 1)
        console.print(f"  {frame}  [dim]Collapsing{dots}[/dim]")

    time.sleep(0.5)
    console.print()

    # Determine collapse outcome
    if _collapse is not None:
        collapsed_to_sorted = _collapse
    elif already_sorted:
        collapsed_to_sorted = False
    else:
        collapsed_to_sorted = random.random() < p_sorted

    result = sorted_state if collapsed_to_sorted else unsorted_state
    comment = random.choice(
        COLLAPSE_COMMENTS_SORTED if collapsed_to_sorted else COLLAPSE_COMMENTS_UNSORTED
    )

    # --- Phase 5: Reveal ---
    if collapsed_to_sorted:
        console.print(Rule(
            "[bold green]✨ Wavefunction collapsed → |sorted⟩[/bold green]",
            style="green",
        ))
        console.print()
        console.print("  [bold green]🐱 The cat lives.[/bold green]")
    else:
        console.print(Rule(
            "[bold magenta]💥 Wavefunction collapsed → |unsorted⟩[/bold magenta]",
            style="magenta",
        ))
        console.print()
        console.print("  [bold magenta]😾 The cat is displeased.[/bold magenta]")

    console.print()

    # Per-element reveal of final positions
    console.print("  [dim]Final state:[/dim]")
    for i, num in enumerate(result):
        time.sleep(0.2)
        col = "green" if collapsed_to_sorted else "magenta"
        console.print(f"    [{col}]position {i}[/{col}] → [bold]{num}[/bold]")

    console.print()
    console.print(f"  [dim italic]\"{comment}\"[/dim italic]")
    console.print()

    return result, collapsed_to_sorted, comment


def create_result_table(original, result, collapsed_to_sorted, comment, meanness, estimated_p_sorted):
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
    table.add_row("Meanness", f"[magenta]{meanness:.2f}[/magenta]")
    table.add_row("Est. p(sorted)", f"[cyan]{estimated_p_sorted:.2f}[/cyan]")
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
