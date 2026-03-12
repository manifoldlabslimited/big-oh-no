#!/usr/bin/env python3
"""
Stalin Sort - A sorting algorithm that eliminates disorder!
Any element out of order is simply... removed.
The survivors form a perfectly sorted list.
"""

import sys
import random
import time

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, IntPrompt, Confirm
from rich.text import Text
from rich.align import Align
from rich import box
from rich.rule import Rule
from rich.live import Live
from rich.columns import Columns

console = Console()

eliminated = []
survivors = []


def create_header():
    """Create a dramatic header panel."""
    title = Text()
    title.append("☭ ", style="red")
    title.append("S T A L I N", style="bold red")
    title.append("   ", style="")
    title.append("S O R T", style="bold yellow")
    title.append(" ☭", style="red")
    
    subtitle = Text("In Soviet Russia, list sorts YOU", style="dim italic")
    
    return Panel(
        Align.center(
            Text.assemble(
                title,
                "\n",
                subtitle,
            )
        ),
        box=box.DOUBLE_EDGE,
        style="bold red",
        padding=(1, 2),
    )


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


def stalin_sort(numbers, animate=True):
    """Sort by eliminating any element that is out of order."""
    global eliminated, survivors
    eliminated = []
    survivors = []
    
    if not numbers:
        return []
    
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
    
    if animate:
        time.sleep(0.5)
    
    console.print(f"[green]✓[/green] [bold cyan]{numbers[0]}[/bold cyan] takes the lead. [dim]Welcome, comrade.[/dim]")
    
    if animate:
        time.sleep(0.3)
    
    for i, num in enumerate(numbers[1:], start=1):
        if animate:
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
    
    return survivors


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


def create_comparison_visual(original, survivors, eliminated):
    """Create a visual comparison of before/after."""
    max_val = max(original) if original else 1
    bar_scale = 25 / max_val
    
    console.print(Panel(
        "[bold]Before vs After[/bold]",
        style="cyan",
        box=box.HEAVY_HEAD,
    ))
    
    # Before - showing which will survive
    console.print("\n[bold yellow]📋 Before (with fates):[/bold yellow]")
    for num in original:
        bar_len = int(num * bar_scale)
        bar = "█" * bar_len
        if num in survivors:
            console.print(f"  [dim]{num:3d}[/dim] │[green]{bar}[/green] [green]✓[/green]")
        else:
            console.print(f"  [dim]{num:3d}[/dim] │[red]{bar}[/red] [red]✗[/red]")
    
    # After
    console.print("\n[bold green]✅ After (survivors only):[/bold green]")
    for num in survivors:
        bar_len = int(num * bar_scale)
        bar = "█" * bar_len
        console.print(f"  [dim]{num:3d}[/dim] │[green]{bar}[/green]")
    
    # Eliminated (graveyard)
    if eliminated:
        console.print("\n[bold red]💀 The Fallen:[/bold red]")
        for num in eliminated:
            bar_len = int(num * bar_scale)
            bar = "░" * bar_len
            console.print(f"  [dim strikethrough]{num:3d}[/dim strikethrough] │[dim]{bar}[/dim]")


def get_numbers_interactively():
    """Get numbers from user interactively."""
    console.print()
    console.print(Panel(
        "[bold]How would you like to provide numbers?[/bold]\n\n"
        "[cyan]1.[/cyan] Enter numbers manually\n"
        "[cyan]2.[/cyan] Generate random numbers\n"
        "[cyan]3.[/cyan] Use example set (high casualties)",
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
                input_str = input_str.replace(",", " ")
                numbers = [int(x.strip()) for x in input_str.split() if x.strip()]
                if not numbers:
                    console.print("[red]Please enter at least one number![/red]")
                    continue
                return numbers
            except ValueError:
                console.print("[red]Invalid input! Please enter numbers only.[/red]")
    
    elif choice == "2":
        count = IntPrompt.ask("[bold cyan]How many numbers?[/bold cyan]", default=10)
        max_val = IntPrompt.ask("[bold cyan]Maximum value?[/bold cyan]", default=20)
        numbers = [random.randint(1, max_val) for _ in range(count)]
        console.print(f"\n[dim]Generated:[/dim] [bold cyan]{numbers}[/bold cyan]")
        return numbers
    
    else:
        # Example with intentionally many out-of-order elements
        return [5, 1, 9, 2, 8, 3, 10, 4, 7, 6]


def main():
    """Main entry point for stalin sort."""
    console.print()
    console.print(create_header())
    
    # Algorithm explanation
    console.print(Panel(
        "[bold]How Stalin Sort Works:[/bold]\n\n"
        "• Iterate through the list from left to right\n"
        "• Keep track of the current maximum value\n"
        "• If an element is [green]>= current max[/green], it [green]survives[/green]\n"
        "• If an element is [red]< current max[/red], it is [red]eliminated[/red]\n"
        "• Result: A sorted list (of survivors)\n\n"
        "[dim]Complexity: O(n) time · O(1) space · O(n) casualties[/dim]",
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
    else:
        # Interactive mode
        numbers = get_numbers_interactively()
    
    # Store original for comparison
    original = numbers.copy()
    
    # Run the sort
    sorted_nums = stalin_sort(numbers)
    
    # Show results
    console.print()
    console.print(Align.center(create_result_table(original, survivors, eliminated)))
    console.print()
    
    create_comparison_visual(original, survivors, eliminated)
    
    # Final summary
    survival_rate = (len(survivors) / len(original)) * 100
    
    if survival_rate == 100:
        verdict = "🎖️  Perfect! The list was already in order. No purge needed."
        style = "green"
    elif survival_rate >= 70:
        verdict = "📈 Acceptable losses. The party is pleased."
        style = "yellow"
    elif survival_rate >= 40:
        verdict = "⚠️  Significant casualties. But order has been achieved."
        style = "yellow"
    else:
        verdict = "💀 Brutal. But necessary."
        style = "red"
    
    console.print()
    console.print(Panel(
        f"[bold {style}]{verdict}[/bold {style}]\n\n"
        f"[dim]Original:[/dim]  {original}\n"
        f"[dim]Sorted:[/dim]    [bold cyan]{survivors}[/bold cyan]\n"
        f"[dim]Eliminated:[/dim] [red]{eliminated}[/red]",
        title="[bold yellow]☭ Final Verdict ☭[/bold yellow]",
        box=box.DOUBLE,
        style=style,
    ))
    
    console.print()
    console.print("[dim]Usage: python stalin_sort.py [num1 num2 ...] or run interactively[/dim]")
    console.print()


if __name__ == "__main__":
    main()
