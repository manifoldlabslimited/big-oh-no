#!/usr/bin/env python3
"""
Wait Sort - A sorting algorithm that sorts by waiting!
Each number waits for a duration proportional to its value,
then announces itself. Smaller numbers finish first = sorted!
"""

import threading
import time
import sys
import random

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn
from rich.table import Table
from rich.prompt import Prompt, IntPrompt, Confirm
from rich.live import Live
from rich.layout import Layout
from rich.text import Text
from rich.align import Align
from rich import box
from rich.style import Style
from rich.rule import Rule

console = Console()

result = []
result_lock = threading.Lock()
start_time = None
completions = {}  # Track which numbers have completed


def create_header():
    """Create a beautiful header panel."""
    from rich.columns import Columns
    
    title = Text()
    title.append("⏳ ", style="yellow")
    title.append("W A I T", style="bold cyan")
    title.append("   ", style="")
    title.append("S O R T", style="bold magenta")
    title.append(" ⏳", style="yellow")
    
    subtitle = Text("The most patient sorting algorithm ever invented", style="dim italic")
    
    return Panel(
        Align.center(
            Text.assemble(
                title,
                "\n",
                subtitle,
            )
        ),
        box=box.DOUBLE_EDGE,
        style="bold blue",
        padding=(1, 2),
    )


def create_stats_table(numbers, scale):
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
    table.add_row("Scale factor", f"[yellow]{scale}s[/yellow] per unit")
    table.add_row("Min value", f"[green]{min(numbers)}[/green]")
    table.add_row("Max value", f"[red]{max(numbers)}[/red]")
    table.add_row("Estimated time", f"[magenta]{max(numbers) * scale:.1f}s[/magenta]")
    
    return table


def wait_and_append_rich(num, scale, progress, task_ids):
    """Wait proportionally to the number, then add to results."""
    wait_time = num * scale
    task_id = task_ids[num]
    
    steps = max(int(wait_time * 20), 1)
    for i in range(steps):
        time.sleep(wait_time / steps)
        progress.update(task_id, completed=i + 1)
    
    with result_lock:
        result.append(num)
        completions[num] = time.time() - start_time
        progress.update(task_id, completed=steps, description=f"[green]✓[/green] [bold]{num}[/bold]")


def wait_sort(numbers, scale=1.0):
    """Sort numbers by making each wait proportionally to its value."""
    global result, start_time, completions
    result = []
    completions = {}
    start_time = time.time()
    
    console.print()
    console.print(create_header())
    console.print()
    console.print(Align.center(create_stats_table(numbers, scale)))
    console.print()
    
    console.print(Rule("[bold cyan]🚀 Starting Sort[/bold cyan]", style="cyan"))
    console.print()
    console.print("[dim]Each number waits (value × scale) seconds before finishing...[/dim]")
    console.print("[dim]Smaller numbers finish first → Natural sorting![/dim]")
    console.print()
    
    max_val = max(numbers)
    
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
        for num in sorted(numbers, reverse=True):  # Show larger numbers at top
            steps = max(int(num * scale * 20), 1)
            task_id = progress.add_task(
                f"[yellow]⏳[/yellow] [bold cyan]{num:3d}[/bold cyan]",
                total=steps,
            )
            task_ids[num] = task_id
        
        # Create threads
        threads = []
        for num in numbers:
            t = threading.Thread(target=wait_and_append_rich, args=(num, scale, progress, task_ids))
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
        wait = completions.get(num, 0)
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


def get_numbers_interactively():
    """Get numbers from user interactively."""
    console.print()
    console.print(Panel(
        "[bold]How would you like to provide numbers?[/bold]\n\n"
        "[cyan]1.[/cyan] Enter numbers manually\n"
        "[cyan]2.[/cyan] Generate random numbers\n"
        "[cyan]3.[/cyan] Use example set",
        title="[bold yellow]🔢 Input Method[/bold yellow]",
        box=box.ROUNDED,
    ))
    
    choice = Prompt.ask(
        "\n[bold cyan]Choose option[/bold cyan]",
        choices=["1", "2", "3"],
        default="1",
    )
    
    if choice == "1":
        console.print("\n[dim]Enter numbers separated by spaces or commas[/dim]")
        while True:
            try:
                input_str = Prompt.ask("[bold cyan]Numbers[/bold cyan]")
                # Parse input - handle spaces, commas, or both
                input_str = input_str.replace(",", " ")
                numbers = [int(x.strip()) for x in input_str.split() if x.strip()]
                if not numbers:
                    console.print("[red]Please enter at least one number![/red]")
                    continue
                if any(n < 0 for n in numbers):
                    console.print("[red]Please use positive numbers only![/red]")
                    continue
                if any(n > 15 for n in numbers):
                    console.print(f"[yellow]⚠️  Numbers >15 will take a while (max wait: {max(numbers)}s)![/yellow]")
                    if not Confirm.ask("Continue anyway?"):
                        continue
                return numbers
            except ValueError:
                console.print("[red]Invalid input! Please enter numbers only.[/red]")
    
    elif choice == "2":
        count = IntPrompt.ask("[bold cyan]How many numbers?[/bold cyan]", default=6)
        max_val = IntPrompt.ask("[bold cyan]Maximum value?[/bold cyan]", default=8)
        numbers = [random.randint(1, max_val) for _ in range(count)]
        console.print(f"\n[dim]Generated:[/dim] [bold cyan]{numbers}[/bold cyan]")
        return numbers
    
    else:
        return [5, 2, 7, 1, 4, 3, 6]


def get_scale_interactively():
    """Get scale factor from user."""
    console.print()
    console.print("[dim]Scale factor determines wait time: number × scale = seconds[/dim]")
    console.print("[dim]Default is 1.0 (each unit = 1 second). Use smaller for faster demo.[/dim]")
    
    scale_input = Prompt.ask(
        "[bold cyan]Scale factor[/bold cyan]",
        default="1.0",
    )
    
    try:
        scale = float(scale_input)
        if scale <= 0:
            console.print("[yellow]Scale must be positive, using 0.1[/yellow]")
            return 0.1
        return scale
    except ValueError:
        console.print("[yellow]Invalid scale, using default 0.1[/yellow]")
        return 0.1


def main():
    """Main entry point for wait sort."""
    console.print()
    console.print(create_header())
    
    # Algorithm explanation
    console.print(Panel(
        "[bold]How Wait Sort Works:[/bold]\n\n"
        "• Each number spawns a thread that [cyan]waits[/cyan] for (number × scale) seconds\n"
        "• Smaller numbers finish waiting [green]first[/green]\n"
        "• Numbers are collected in the order they finish\n"
        "• Result: [bold green]Naturally sorted![/bold green]\n\n"
        "[dim]Complexity: O(max(n)) time · O(n) threads · 100% patience required[/dim]",
        title="[bold cyan]💡 Algorithm Explanation[/bold cyan]",
        box=box.ROUNDED,
        padding=(1, 2),
    ))
    
    # Check for command line arguments
    if len(sys.argv) > 1:
        try:
            numbers = [int(x) for x in sys.argv[1:]]
            console.print(f"\n[dim]Using command line arguments:[/dim] [bold cyan]{numbers}[/bold cyan]")
        except ValueError:
            console.print("[red]Error: Please provide valid integers as arguments[/red]")
            sys.exit(1)
        scale = 1.0
    else:
        # Interactive mode
        numbers = get_numbers_interactively()
        scale = get_scale_interactively()
    
    # Run the sort
    sorted_nums, total_time = wait_sort(numbers, scale)
    
    # Show results
    console.print(Align.center(create_result_table(numbers, sorted_nums, completions)))
    console.print()
    
    create_comparison_bars(numbers, sorted_nums)
    
    # Final summary
    console.print()
    console.print(Panel(
        f"[bold green]✨ Sorted {len(numbers)} numbers in {total_time:.2f} seconds![/bold green]\n\n"
        f"[dim]Original:[/dim] {numbers}\n"
        f"[dim]Sorted:[/dim]   [bold cyan]{sorted_nums}[/bold cyan]",
        title="[bold yellow]🎉 Success![/bold yellow]",
        box=box.DOUBLE,
        style="green",
    ))
    
    console.print()
    console.print("[dim]Usage: python wait_sort.py [num1 num2 ...] or run interactively[/dim]")
    console.print()


if __name__ == "__main__":
    main()
