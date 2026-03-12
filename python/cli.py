#!/usr/bin/env python3
"""
Big O(No) - CLI for utterly useless yet entertaining sorting algorithms.
"""

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box
from rich.align import Align

console = Console()


def show_banner():
    """Display the Big O(No) banner."""
    banner = """
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║   ██████╗ ██╗ ██████╗      ██████╗ ██╗███╗   ██╗ ██████╗ ██╗  ║
    ║   ██╔══██╗██║██╔════╝     ██╔═══██╗╚██╗██╔╝ ██║██╔═══██╗██║   ║
    ║   ██████╔╝██║██║  ███╗    ██║   ██║ ╚███╔╝  ██║██║   ██║██║   ║
    ║   ██╔══██╗██║██║   ██║    ██║   ██║ ██╔██╗  ██║██║   ██║╚═╝   ║
    ║   ██████╔╝██║╚██████╔╝    ╚██████╔╝██╔╝ ██╗ ██║╚██████╔╝██╗   ║
    ║   ╚═════╝ ╚═╝ ╚═════╝      ╚═════╝ ╚═╝  ╚═╝ ╚═╝ ╚═════╝ ╚═╝   ║
    ║                                                               ║
    ║          Utterly Useless Yet Entertaining Sorting             ║
    ╚═══════════════════════════════════════════════════════════════╝
    """
    console.print(f"[bold cyan]{banner}[/bold cyan]")


def show_algorithms_table():
    """Display available algorithms in a nice table."""
    table = Table(
        title="🎭 Available Sorting Algorithms",
        box=box.ROUNDED,
        title_style="bold yellow",
        show_header=True,
        header_style="bold cyan",
    )
    
    table.add_column("Name", style="bold green")
    table.add_column("Persona", style="cyan")
    table.add_column("Method", style="dim")
    table.add_column("Complexity", style="magenta")
    
    table.add_row(
        "wait",
        "⏳ The Patient One",
        "Each number waits (value × scale) seconds",
        "O(max(n)) time",
    )
    table.add_row(
        "stalin",
        "☭ The Authoritarian",
        "Eliminates out-of-order elements",
        "O(n) time, O(n) casualties",
    )
    table.add_row(
        "linus",
        "🐧 The Code Reviewer",
        "NAKs patches that break monotonic order",
        "O(n) time, O(n) hurt feelings",
    )
    
    console.print(table)


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """
    Big O(No) - A collection of utterly useless yet entertaining sorting algorithms.
    
    Each algorithm has its own persona and unique way of achieving "sorted" results.
    Some may lose data. Some may take forever. All are completely impractical.
    
    \b
    Examples:
        big-oh-no wait 5 2 8 1 3
        big-oh-no stalin 5 1 9 2 8 3 10
        big-oh-no linus 3 1 7 2 9 5 12
    """
    if ctx.invoked_subcommand is None:
        show_banner()
        console.print()
        show_algorithms_table()
        console.print()
        console.print("[dim]Run 'big-oh-no --help' for usage or 'big-oh-no <algorithm> --help' for algorithm details[/dim]")


@cli.command(name="list")
def list_algorithms():
    """List all available sorting algorithms."""
    show_banner()
    console.print()
    show_algorithms_table()


@cli.command()
@click.argument('numbers', nargs=-1, type=int)
@click.option('--scale', '-s', default=1.0, help='Scale factor for wait time (default: 1.0 = real seconds)')
@click.option('--interactive', '-i', is_flag=True, help='Run in interactive mode')
def wait(numbers, scale, interactive):
    """
    ⏳ Wait Sort - The most patient sorting algorithm.
    
    Each number spawns a thread that waits for (value × scale) seconds.
    Smaller numbers finish first, resulting in a sorted output.
    
    \b
    Examples:
        big-oh-no wait 5 2 8 1 3
        big-oh-no wait 10 5 3 --scale 0.5
        big-oh-no wait -i
    """
    import wait_sort as ws
    
    if interactive or len(numbers) == 0:
        ws.main()
    else:
        nums = [n for n in numbers]
        
        ws.console.print()
        ws.console.print(ws.create_header())
        
        ws.console.print(Panel(
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
        
        ws.console.print(f"\n[dim]Numbers:[/dim] [bold cyan]{nums}[/bold cyan]")
        ws.console.print(f"[dim]Scale:[/dim] [bold yellow]{scale}s[/bold yellow] per unit")
        
        sorted_nums, total_time = ws.wait_sort(nums, scale)
        
        ws.console.print(Align.center(ws.create_result_table(nums, sorted_nums, ws.completions)))
        ws.console.print()
        ws.create_comparison_bars(nums, sorted_nums)
        
        ws.console.print()
        ws.console.print(Panel(
            f"[bold green]✨ Sorted {len(nums)} numbers in {total_time:.2f} seconds![/bold green]\n\n"
            f"[dim]Original:[/dim] {nums}\n"
            f"[dim]Sorted:[/dim]   [bold cyan]{sorted_nums}[/bold cyan]",
            title="[bold yellow]🎉 Success![/bold yellow]",
            box=box.DOUBLE,
            style="green",
        ))
        ws.console.print()


@cli.command()
@click.argument('numbers', nargs=-1, type=int)
@click.option('--interactive', '-i', is_flag=True, help='Run in interactive mode')
@click.option('--no-animate', is_flag=True, help='Disable animation')
def stalin(numbers, interactive, no_animate):
    """
    ☭ Stalin Sort - Order through elimination.
    
    Iterates through the list and eliminates any element that is smaller
    than the current maximum. Survivors form a sorted list.
    
    \b
    Examples:
        big-oh-no stalin 5 1 9 2 8 3 10
        big-oh-no stalin -i
    """
    import stalin_sort as ss
    
    if interactive or len(numbers) == 0:
        ss.main()
    else:
        nums = [n for n in numbers]
        original = nums.copy()
        
        ss.console.print()
        ss.console.print(ss.create_header())
        
        ss.console.print(Panel(
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
        
        ss.console.print(f"\n[dim]Numbers:[/dim] [bold cyan]{nums}[/bold cyan]")
        
        sorted_nums = ss.stalin_sort(nums, animate=not no_animate)
        
        ss.console.print()
        ss.console.print(Align.center(ss.create_result_table(original, ss.survivors, ss.eliminated)))
        ss.console.print()
        ss.create_comparison_visual(original, ss.survivors, ss.eliminated)
        
        survival_rate = (len(ss.survivors) / len(original)) * 100
        
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
        
        ss.console.print()
        ss.console.print(Panel(
            f"[bold {style}]{verdict}[/bold {style}]\n\n"
            f"[dim]Original:[/dim]  {original}\n"
            f"[dim]Sorted:[/dim]    [bold cyan]{ss.survivors}[/bold cyan]\n"
            f"[dim]Eliminated:[/dim] [red]{ss.eliminated}[/red]",
            title="[bold yellow]☭ Final Verdict ☭[/bold yellow]",
            box=box.DOUBLE,
            style=style,
        ))
        ss.console.print()


@cli.command()
@click.argument('numbers', nargs=-1, type=int)
@click.option('--interactive', '-i', is_flag=True, help='Run in interactive mode')
@click.option('--no-animate', is_flag=True, help='Disable animation')
def linus(numbers, interactive, no_animate):
    """
    🐧 Linus Sort - Code review with maximum hostility.
    
    Each element is reviewed by a simulated Linus Torvalds.
    Elements that break monotonic order get NAK'd with colorful commentary.
    
    \b
    Examples:
        big-oh-no linus 3 1 7 2 9 5 12
        big-oh-no linus -i
    """
    import linus_sort as ls
    
    if interactive or len(numbers) == 0:
        ls.main()
    else:
        nums = [n for n in numbers]
        original = nums.copy()
        
        ls.console.print()
        ls.console.print(ls.create_header())
        
        ls.console.print(Panel(
            "[bold]How Linus Sort Works:[/bold]\n\n"
            "• Submit your patches (numbers) for review\n"
            "• Linus reviews each one with [red]brutal honesty[/red]\n"
            "• Patches must maintain [cyan]monotonic order[/cyan] to be merged\n"
            "• Out-of-order patches get [red]NAK'd[/red] with colorful commentary\n"
            "• Result: A sorted list (of surviving patches)\n\n"
            "[dim]Complexity: O(n) time · O(1) space · O(n) hurt feelings[/dim]",
            title="[bold cyan]💡 Review Process[/bold cyan]",
            box=box.ROUNDED,
            padding=(1, 2),
        ))
        
        ls.console.print(f"\n[dim]Patches submitted:[/dim] [bold cyan]{nums}[/bold cyan]")
        
        sorted_nums = ls.linus_sort(nums, animate=not no_animate)
        
        ls.console.print()
        ls.console.print(Align.center(ls.create_result_table(original, ls.approved, ls.rejected)))
        ls.console.print()
        ls.create_comparison_visual(original, ls.approved, ls.rejected)
        
        acceptance_rate = (len(ls.approved) / len(original)) * 100
        
        if acceptance_rate == 100:
            verdict = "All patches merged. Don't expect this to happen again."
            signature = "- Linus\n\nP.S. I must be in a good mood today."
            style = "green"
        elif acceptance_rate >= 70:
            verdict = "Most of your patches were acceptable. The rest were garbage."
            signature = "- Linus\n\nP.S. Stop wasting my time with obvious bugs."
            style = "yellow"
        elif acceptance_rate >= 40:
            verdict = "More than half your submission was crap. Do better."
            signature = "- Linus\n\nP.S. Maybe consider a different career."
            style = "yellow"
        else:
            verdict = "Your submission is an embarrassment. I expected nothing and was still disappointed."
            signature = "- Linus\n\nP.S. Please never contribute again."
            style = "red"
        
        ls.console.print()
        ls.console.print(Panel(
            f"[bold {style}]{verdict}[/bold {style}]\n\n"
            f"[dim]Submitted:[/dim]  {original}\n"
            f"[dim]Merged:[/dim]     [bold cyan]{ls.approved}[/bold cyan]\n"
            f"[dim]NAK'd:[/dim]      [red]{ls.rejected}[/red]\n\n"
            f"[dim italic]{signature}[/dim italic]",
            title="[bold yellow]🐧 Final Review Comments 🐧[/bold yellow]",
            box=box.DOUBLE,
            style=style,
        ))
        ls.console.print()


def main():
    """Entry point for the CLI."""
    cli()


if __name__ == "__main__":
    main()
