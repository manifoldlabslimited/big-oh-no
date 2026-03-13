#!/usr/bin/env python3
"""
Wait Sort - A sorting algorithm that sorts by waiting!
Each number waits for a duration proportional to its value,
then announces itself. Smaller numbers finish first = sorted!
"""

import threading
import time

from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn
from rich.table import Table
from rich.align import Align
from rich import box
from rich.rule import Rule

from .utils import console, make_sort_header

SCALE = 1.0

result = []
result_lock = threading.Lock()
start_time = None
completions = []  # Completion times aligned with result order


def create_header():
    return make_sort_header("⏳", "wait", "The most patient sorting algorithm ever invented", "cyan")


def create_stats_table(numbers):
    """Create a stats table for the input."""
    table = Table(
        title="📊 Sort Configuration",
        box=box.ROUNDED,
        title_style="bold yellow",
        show_header=True,
        header_style="bold cyan",
    )
    
    table.add_column("Property", style="dim")
    table.add_column("Value", style="green")
    
    table.add_row("Numbers to sort", f"[bold]{numbers}[/bold]")
    table.add_row("Count", f"[cyan]{len(numbers)}[/cyan] numbers")
    table.add_row("Min value", f"[green]{min(numbers)}[/green]")
    table.add_row("Max value", f"[red]{max(numbers)}[/red]")
    table.add_row("Estimated time", f"[magenta]{max(numbers) * SCALE:.1f}s[/magenta]")
    
    return table


def wait_and_append_rich(index, num, progress, task_ids):
    """Wait proportionally to the number, then add to results."""
    wait_time = num * SCALE
    task_id = task_ids[index]
    
    steps = max(int(wait_time * 20), 1)
    for i in range(steps):
        time.sleep(wait_time / steps)
        progress.update(task_id, completed=i + 1)
    
    with result_lock:
        result.append(num)
        completions.append(time.time() - start_time)
        progress.update(task_id, completed=steps, description=f"[green]✓[/green] [bold]{num}[/bold]")


def wait_sort(numbers):
    """Sort numbers by making each wait proportionally to its value."""
    global result, start_time, completions
    result = []
    completions = []
    start_time = time.time()
    indexed_numbers = list(enumerate(numbers))
    
    console.print()
    console.print(create_header())
    console.print()
    console.print(Align.center(create_stats_table(numbers)))
    console.print()
    
    console.print(Rule("[bold cyan]🚀 Starting Sort[/bold cyan]", style="cyan"))
    console.print()
    console.print("[dim]Each number waits (value × scale) seconds before finishing...[/dim]")
    console.print("[dim]Smaller numbers finish first → Natural sorting![/dim]")
    console.print()
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=40, style="cyan", complete_style="green", finished_style="green"),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        console=console,
        expand=False,
    ) as progress:
        
        # Create tasks for each number
        task_ids = {}
        for idx, num in sorted(indexed_numbers, key=lambda item: item[1], reverse=True):
            steps = max(int(num * SCALE * 20), 1)
            task_id = progress.add_task(
                f"[yellow]⏳[/yellow] [bold cyan]{num:3d}[/bold cyan]",
                total=steps,
            )
            task_ids[idx] = task_id
        
        # Create threads
        threads = []
        for idx, num in indexed_numbers:
            t = threading.Thread(target=wait_and_append_rich, args=(idx, num, progress, task_ids))
            threads.append(t)
        
        # Start all threads
        for t in threads:
            t.start()
        
        # Wait for all threads
        for t in threads:
            t.join()
    
    total_time = time.time() - start_time
    
    console.print()
    console.print(Rule("[bold green]✨ Sort Complete![/bold green]", style="green"))
    console.print()
    
    return result, total_time


def create_result_table(original, sorted_nums, completions):
    """Create a beautiful result table."""
    table = Table(
        title="🏆 Finishing Order",
        box=box.ROUNDED,
        title_style="bold green",
        show_header=True,
        header_style="bold cyan",
    )
    
    table.add_column("Place", style="bold yellow", justify="center")
    table.add_column("Number", style="cyan", justify="center")
    table.add_column("Wait Time", style="magenta", justify="right")
    table.add_column("Medal", justify="center")
    
    medals = ["🥇", "🥈", "🥉"] + ["  "] * 100
    
    for i, num in enumerate(sorted_nums):
        wait = completions[i] if i < len(completions) else 0
        table.add_row(
            f"{i + 1}",
            f"[bold]{num}[/bold]",
            f"{wait:.2f}s",
            medals[i] if i < len(medals) else "",
        )
    
    return table


def create_comparison_bars(original, sorted_nums):
    """Create visual bar comparison."""
    max_val = max(original)
    bar_scale = 30 / max_val  # Scale bars to fit
    
    console.print(Panel(
        "[bold]Before vs After[/bold]",
        style="cyan",
        box=box.HEAVY_HEAD,
    ))
    
    # Before
    console.print("\n[bold yellow]📋 Before (unsorted):[/bold yellow]")
    for num in original:
        bar_len = int(num * bar_scale)
        bar = "█" * bar_len
        console.print(f"  [dim]{num:3d}[/dim] │[magenta]{bar}[/magenta]")
    
    # After
    console.print("\n[bold green]✅ After (sorted):[/bold green]")
    for num in sorted_nums:
        bar_len = int(num * bar_scale)
        bar = "█" * bar_len
        console.print(f"  [dim]{num:3d}[/dim] │[green]{bar}[/green]")
