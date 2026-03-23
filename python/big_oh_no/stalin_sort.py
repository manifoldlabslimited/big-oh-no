#!/usr/bin/env python3
"""
Stalin Sort - A sorting algorithm that eliminates disorder!
Any element out of order is simply... removed.
The survivors form a perfectly sorted list.
"""

import time

from rich.panel import Panel
from rich.table import Table
from rich.align import Align
from rich import box
from rich.rule import Rule

from .utils import console, make_sort_header


def create_header():
    return make_sort_header("☭", "stalin", "In Soviet Russia, list sorts YOU", "red")


def create_stats_table(numbers):
    """Create a stats table for the input."""
    table = Table(
        title="📋 Input Analysis",
        box=box.ROUNDED,
        title_style="bold yellow",
        show_header=True,
        header_style="bold cyan",
    )
    
    table.add_column("Property", style="dim")
    table.add_column("Value", style="green")
    
    table.add_row("Numbers to sort", f"[bold]{numbers}[/bold]")
    table.add_row("Count", f"[cyan]{len(numbers)}[/cyan] elements")
    table.add_row("Min value", f"[green]{min(numbers)}[/green]")
    table.add_row("Max value", f"[red]{max(numbers)}[/red]")
    
    return table


def stalin_sort(numbers):
    """Sort by eliminating any element that is out of order."""
    eliminated = []
    survivors = []
    
    console.print()
    console.print(create_header())
    console.print()
    console.print(Align.center(create_stats_table(numbers)))
    console.print()
    
    console.print(Rule("[bold red]⚔️ Beginning The Purge ⚔️[/bold red]", style="red"))
    console.print()
    console.print("[dim]Any element smaller than the previous will be... [red]eliminated[/red][/dim]")
    console.print()
    
    # The sorting process
    current_max = numbers[0]
    survivors.append(numbers[0])
    
    time.sleep(0.5)
    
    console.print(f"[green]✓[/green] [bold cyan]{numbers[0]}[/bold cyan] takes the lead. [dim]Welcome, comrade.[/dim]")
    
    time.sleep(0.3)
    
    for num in numbers[1:]:
        time.sleep(0.4)
        
        if num >= current_max:
            survivors.append(num)
            current_max = num
            console.print(f"[green]✓[/green] [bold cyan]{num}[/bold cyan] maintains order. [dim]Approved.[/dim]")
        else:
            eliminated.append(num)
            console.print(f"[red]✗[/red] [bold red]{num}[/bold red] is out of order! [dim italic]Eliminated.[/dim italic] 💀")
    
    console.print()
    console.print(Rule("[bold green]✨ Purge Complete ✨[/bold green]", style="green"))
    
    return survivors, eliminated


def create_result_table(original, survivors, eliminated):
    """Create a results summary table."""
    table = Table(
        title="📊 Final Report",
        box=box.ROUNDED,
        title_style="bold yellow",
        show_header=True,
        header_style="bold cyan",
    )
    
    table.add_column("Category", style="dim")
    table.add_column("Count", justify="center")
    table.add_column("Elements", style="cyan")
    
    table.add_row(
        "[bold]Original[/bold]",
        str(len(original)),
        str(original),
    )
    table.add_row(
        "[green]✓ Survivors[/green]",
        f"[green]{len(survivors)}[/green]",
        f"[green]{survivors}[/green]",
    )
    table.add_row(
        "[red]✗ Eliminated[/red]",
        f"[red]{len(eliminated)}[/red]",
        f"[red]{eliminated}[/red]" if eliminated else "[dim]None[/dim]",
    )
    
    survival_rate = (len(survivors) / len(original)) * 100
    table.add_row(
        "[bold yellow]Survival Rate[/bold yellow]",
        f"[yellow]{survival_rate:.1f}%[/yellow]",
        create_survival_bar(survival_rate),
    )
    
    return table


def create_survival_bar(percentage):
    """Create a visual survival rate bar."""
    bar_width = 20
    filled = int(bar_width * percentage / 100)
    empty = bar_width - filled
    
    if percentage >= 80:
        color = "green"
    elif percentage >= 50:
        color = "yellow"
    else:
        color = "red"
    
    return f"[{color}]{'█' * filled}[/{color}][dim]{'░' * empty}[/dim]"


def _bar(value, scale, char="█"):
    return char * int(value * scale)


def create_comparison_visual(original, survivors, eliminated):
    """Create a visual comparison of before/after."""
    max_val = max(original) if original else 1
    scale = 25 / max_val
    # Build a mutable copy so we can mark off duplicates correctly.
    remaining_eliminated = list(eliminated)

    console.print(Panel(
        "[bold]Before vs After[/bold]",
        style="cyan",
        box=box.HEAVY_HEAD,
    ))

    console.print("\n[bold yellow]📋 Before (with fates):[/bold yellow]")
    for num in original:
        if num in remaining_eliminated:
            remaining_eliminated.remove(num)
            console.print(f"  [dim]{num:3d}[/dim] │[red]{_bar(num, scale)}[/red] [red]✗[/red]")
        else:
            console.print(f"  [dim]{num:3d}[/dim] │[green]{_bar(num, scale)}[/green] [green]✓[/green]")

    console.print("\n[bold green]✅ After (survivors only):[/bold green]")
    for num in survivors:
        console.print(f"  [dim]{num:3d}[/dim] │[green]{_bar(num, scale)}[/green]")

    if eliminated:
        console.print("\n[bold red]💀 The Fallen:[/bold red]")
        for num in eliminated:
            console.print(f"  [dim strikethrough]{num:3d}[/dim strikethrough] │[dim]{_bar(num, scale, '░')}[/dim]")


# ── Visualization generator ──────────────────────────────────────────────────

def stalin_sort_viz(numbers, result=None):
    """Generator that yields VizFrames for the visualization.

    Same logic as stalin_sort but yields a frame per element inspected.
    Each frame includes a log_line for the running text log.

    Pass a dict as *result* to receive ``{"survivors": [...], "eliminated": [...]}``
    once the generator is exhausted.
    """
    from .visualizer import Action, VizFrame

    bars = list(numbers)
    n = len(bars)
    eliminated = []

    yield VizFrame(bars=list(bars), highlighted=[], action=Action.COMPARE,
                   label="Inspecting the population...",
                   log_line="[dim]Beginning the purge...[/dim]")

    current_max = bars[0]

    yield VizFrame(bars=list(bars), highlighted=[0], action=Action.PLACE,
                   label=f"{bars[0]} takes the lead. Welcome, comrade.",
                   log_line=f"[green]✓[/green] [bold cyan]{bars[0]}[/bold cyan] takes the lead. [dim]Welcome, comrade.[/dim]")

    i = 1
    while i < len(bars):
        yield VizFrame(bars=list(bars), highlighted=[i], action=Action.COMPARE,
                       label=f"Inspecting {bars[i]}...")

        if bars[i] >= current_max:
            current_max = bars[i]
            yield VizFrame(bars=list(bars), highlighted=[i], action=Action.PLACE,
                           label=f"{bars[i]} maintains order. Approved.",
                           log_line=f"[green]✓[/green] [bold cyan]{bars[i]}[/bold cyan] maintains order. [dim]Approved.[/dim]")
            i += 1
        else:
            val = bars[i]
            eliminated.append(val)
            yield VizFrame(bars=list(bars), highlighted=[i], action=Action.ELIMINATE,
                           label=f"{val} is out of order! Eliminated. 💀",
                           log_line=f"[red]✗[/red] [bold red]{val}[/bold red] is out of order! [dim italic]Eliminated.[/dim italic] 💀")
            bars.pop(i)

    yield VizFrame(bars=list(bars), highlighted=list(range(len(bars))), action=Action.DONE,
                   label=f"Purge complete. {len(bars)}/{n} survived.",
                   log_line=f"\n[bold green]✨ Purge complete. {len(bars)}/{n} survived.[/bold green]")

    if result is not None:
        result["survivors"] = list(bars)
        result["eliminated"] = eliminated
