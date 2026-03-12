#!/usr/bin/env python3
"""
Linus Torvalds Code Review Sort - A sorting algorithm with BRUTAL code reviews!
Elements are reviewed by a simulated Linus and rejected with increasingly
angry comments if they don't meet his exacting standards.
"""

import sys
import random
import time

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, IntPrompt
from rich.text import Text
from rich.align import Align
from rich import box
from rich.rule import Rule

console = Console()

rejected = []
approved = []
review_log = []

# Linus-style rejection messages (inspired by actual LKML quotes)
REJECTION_MESSAGES = [
    "Christ people. This is just sh*t.",
    "Your code is bad and you should feel bad.",
    "This is GARBAGE. I'm not even going to try.",
    "What drugs are you on? Can I have some?",
    "This is not 'quality code'. This is 'I don't know what I'm doing' code.",
    "Please remove your whose whose whose whose whose whose whose piece of crap.",
    "Do you really think this is acceptable? Honestly?",
    "This is SO BROKEN. Just... no.",
    "I'm not touching this steaming pile of crap.",
    "This makes me want to mass delete your contribution.",
    "This is a prime example of how NOT to do things.",
    "Did you even TEST this? Of course you didn't.",
    "Your taste is clearly broken.",
    "This code is an abortion. Fix it.",
    "I'd rather use a typewriter than this mess.",
    "This is pure, unadulterated garbage.",
]

# Linus-style approval messages (rare and begrudging)
APPROVAL_MESSAGES = [
    "Fine. It's acceptable. Barely.",
    "I suppose this doesn't completely suck.",
    "Okay, this one can stay. Don't let it go to your head.",
    "Finally, someone who isn't completely incompetent.",
    "This is... actually not terrible. I'm shocked.",
    "Acceptable. But don't think you're special.",
    "Hmph. This one passes. Barely.",
    "I've seen worse. Much worse. Fine.",
]

# Technical rejection reasons
REJECTION_REASONS = [
    "breaks binary compatibility",
    "has undefined behavior",
    "uses tabs where spaces should be",
    "is too clever by half",
    "violates kernel coding style",
    "looks like enterprise Java crap",
    "smells like Windows code",
    "is an abomination unto computing",
    "makes baby Tux cry",
    "would make the kernel slower",
    "has the stench of overengineering",
    "is a crime against humanity",
]


def create_header():
    """Create an intimidating header panel."""
    title = Text()
    title.append("🐧 ", style="yellow")
    title.append("L I N U S", style="bold white")
    title.append("   ", style="")
    title.append("S O R T", style="bold cyan")
    title.append(" 🐧", style="yellow")
    
    subtitle = Text("Code Review Mode: MAXIMUM HOSTILITY", style="red italic")
    
    return Panel(
        Align.center(
            Text.assemble(
                title,
                "\n",
                subtitle,
            )
        ),
        box=box.DOUBLE_EDGE,
        style="bold yellow",
        padding=(1, 2),
    )


def create_stats_table(numbers):
    """Create input analysis table."""
    table = Table(
        title="📋 Submissions for Review",
        box=box.ROUNDED,
        title_style="bold cyan",
        show_header=True,
        header_style="bold yellow",
    )
    
    table.add_column("Property", style="dim")
    table.add_column("Value", style="cyan")
    
    table.add_row("Submitted elements", f"[bold]{numbers}[/bold]")
    table.add_row("Count", f"[cyan]{len(numbers)}[/cyan] patches")
    table.add_row("Reviewer mood", f"[red]{'😤' * random.randint(3, 5)} GRUMPY[/red]")
    table.add_row("Coffee level", f"[yellow]{'☕' * random.randint(1, 3)} LOW[/yellow]")
    
    return table


def get_rejection_reason(num, prev_max):
    """Generate a technical-sounding rejection reason."""
    reasons = [
        f"is {num}, which breaks binary compatibility with {prev_max}",
        f"at {num} is clearly wrong when we need >= {prev_max}",
        f"({num}) violates monotonic ordering principles",
        f"of value {num} {random.choice(REJECTION_REASONS)}",
        f"({num} < {prev_max}) - can you even COUNT?!",
    ]
    return random.choice(reasons)


def linus_sort(numbers, animate=True):
    """Sort by having Linus review each element."""
    global rejected, approved, review_log
    rejected = []
    approved = []
    review_log = []
    
    if not numbers:
        return []
    
    console.print()
    console.print(create_header())
    console.print()
    console.print(Align.center(create_stats_table(numbers)))
    console.print()
    
    # Email header style
    console.print(Panel(
        "[dim]From:[/dim] [bold]Linus Torvalds <torvalds@linux-foundation.org>[/bold]\n"
        "[dim]To:[/dim] [bold]LKML <linux-kernel@vger.kernel.org>[/bold]\n"
        "[dim]Subject:[/dim] [bold red]Re: [PATCH] Your terrible sorting submission[/bold red]",
        box=box.ROUNDED,
        style="dim",
    ))
    console.print()
    
    console.print(Rule("[bold red]📧 Code Review in Progress[/bold red]", style="red"))
    console.print()
    
    current_max = numbers[0]
    approved.append(numbers[0])
    
    if animate:
        time.sleep(0.5)
    
    # First element always passes (begrudgingly)
    msg = random.choice(APPROVAL_MESSAGES)
    console.print(f"[green]✓[/green] [bold cyan]{numbers[0]}[/bold cyan]")
    console.print(f"  [dim italic]\"{msg}\"[/dim italic]")
    console.print(f"  [dim]- Linus[/dim]")
    review_log.append((numbers[0], True, msg))
    
    if animate:
        time.sleep(0.3)
    
    for num in numbers[1:]:
        if animate:
            time.sleep(0.5)
        
        console.print()
        
        if num >= current_max:
            approved.append(num)
            current_max = num
            msg = random.choice(APPROVAL_MESSAGES)
            console.print(f"[green]✓[/green] [bold cyan]{num}[/bold cyan]")
            console.print(f"  [dim italic]\"{msg}\"[/dim italic]")
            console.print(f"  [dim]- Linus[/dim]")
            review_log.append((num, True, msg))
        else:
            rejected.append(num)
            reason = get_rejection_reason(num, current_max)
            rant = random.choice(REJECTION_MESSAGES)
            
            console.print(f"[red]✗[/red] [bold red]{num}[/bold red] [red]REJECTED[/red]")
            console.print(f"  [red bold]\"{rant}\"[/red bold]")
            console.print(f"  [dim]This patch {reason}.[/dim]")
            console.print(f"  [dim]NAK. Not applying.[/dim]")
            console.print(f"  [dim]- Linus[/dim]")
            review_log.append((num, False, rant))
    
    console.print()
    console.print(Rule("[bold green]📧 Review Complete[/bold green]", style="green"))
    
    return approved


def create_result_table(original, approved, rejected):
    """Create review summary table."""
    table = Table(
        title="📊 Review Summary",
        box=box.ROUNDED,
        title_style="bold yellow",
        show_header=True,
        header_style="bold cyan",
    )
    
    table.add_column("Status", style="dim")
    table.add_column("Count", justify="center")
    table.add_column("Patches", style="cyan")
    
    table.add_row(
        "[bold]Submitted[/bold]",
        str(len(original)),
        str(original),
    )
    table.add_row(
        "[green]✓ Merged[/green]",
        f"[green]{len(approved)}[/green]",
        f"[green]{approved}[/green]",
    )
    table.add_row(
        "[red]✗ NAK'd[/red]",
        f"[red]{len(rejected)}[/red]",
        f"[red]{rejected}[/red]" if rejected else "[dim]None[/dim]",
    )
    
    acceptance_rate = (len(approved) / len(original)) * 100
    
    # Linus mood based on rejection rate
    if acceptance_rate == 100:
        mood = "[green]😐 Mildly Satisfied[/green]"
    elif acceptance_rate >= 70:
        mood = "[yellow]😤 Annoyed[/yellow]"
    elif acceptance_rate >= 40:
        mood = "[red]😠 Angry[/red]"
    else:
        mood = "[red bold]🤬 RAGE MODE[/red bold]"
    
    table.add_row("Acceptance Rate", f"{acceptance_rate:.1f}%", mood)
    
    return table


def create_comparison_visual(original, approved, rejected):
    """Create visual diff of merged vs rejected."""
    max_val = max(original) if original else 1
    bar_scale = 25 / max_val
    
    console.print(Panel(
        "[bold]Merge Status Diff[/bold]",
        style="cyan",
        box=box.HEAVY_HEAD,
    ))
    
    # Git-style diff
    console.print("\n[bold yellow]📝 git log --oneline:[/bold yellow]")
    for num in original:
        bar_len = int(num * bar_scale)
        bar = "█" * bar_len
        if num in approved:
            console.print(f"  [green]+[/green] [dim]{num:3d}[/dim] │[green]{bar}[/green] [green]merged[/green]")
        else:
            console.print(f"  [red]-[/red] [dim]{num:3d}[/dim] │[red]{bar}[/red] [red]dropped[/red]")
    
    # Final tree
    console.print("\n[bold green]🌲 Final tree (master):[/bold green]")
    for num in approved:
        bar_len = int(num * bar_scale)
        bar = "█" * bar_len
        console.print(f"  [dim]{num:3d}[/dim] │[green]{bar}[/green]")
    
    # Rejected patches
    if rejected:
        console.print("\n[bold red]🗑️ Rejected patches (in recycling bin):[/bold red]")
        for num in rejected:
            bar_len = int(num * bar_scale)
            bar = "░" * bar_len
            console.print(f"  [dim strikethrough]{num:3d}[/dim strikethrough] │[dim]{bar}[/dim]")


def get_numbers_interactively():
    """Get numbers from user interactively."""
    console.print()
    console.print(Panel(
        "[bold]Submit your patches for review:[/bold]\n\n"
        "[cyan]1.[/cyan] Enter patch numbers manually\n"
        "[cyan]2.[/cyan] Generate random submissions\n"
        "[cyan]3.[/cyan] Use example (typical kernel submission)",
        title="[bold yellow]📬 Patch Submission[/bold yellow]",
        box=box.ROUNDED,
    ))
    
    choice = Prompt.ask(
        "\n[bold cyan]Choose option[/bold cyan]",
        choices=["1", "2", "3"],
        default="1",
    )
    
    if choice == "1":
        console.print("\n[dim]Enter patch numbers separated by spaces or commas[/dim]")
        while True:
            try:
                input_str = Prompt.ask("[bold cyan]Patches[/bold cyan]")
                input_str = input_str.replace(",", " ")
                numbers = [int(x.strip()) for x in input_str.split() if x.strip()]
                if not numbers:
                    console.print("[red]Submit at least one patch![/red]")
                    continue
                return numbers
            except ValueError:
                console.print("[red]Invalid input! Patch IDs must be numbers.[/red]")
    
    elif choice == "2":
        count = IntPrompt.ask("[bold cyan]How many patches?[/bold cyan]", default=8)
        max_val = IntPrompt.ask("[bold cyan]Maximum patch ID?[/bold cyan]", default=15)
        numbers = [random.randint(1, max_val) for _ in range(count)]
        console.print(f"\n[dim]Generated submission:[/dim] [bold cyan]{numbers}[/bold cyan]")
        return numbers
    
    else:
        return [3, 1, 7, 2, 9, 5, 12, 4, 8]


def main():
    """Main entry point for linus sort."""
    console.print()
    console.print(create_header())
    
    # Intro Panel
    console.print(Panel(
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
    
    # Check for command line arguments
    if len(sys.argv) > 1:
        try:
            numbers = [int(x) for x in sys.argv[1:]]
            console.print(f"\n[dim]Patches submitted:[/dim] [bold cyan]{numbers}[/bold cyan]")
        except ValueError:
            console.print("[red]Error: Patch IDs must be valid integers[/red]")
            sys.exit(1)
    else:
        numbers = get_numbers_interactively()
    
    original = numbers.copy()
    
    # Run the review
    sorted_nums = linus_sort(numbers)
    
    # Show results
    console.print()
    console.print(Align.center(create_result_table(original, approved, rejected)))
    console.print()
    
    create_comparison_visual(original, approved, rejected)
    
    # Final verdict
    acceptance_rate = (len(approved) / len(original)) * 100
    
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
    
    console.print()
    console.print(Panel(
        f"[bold {style}]{verdict}[/bold {style}]\n\n"
        f"[dim]Submitted:[/dim]  {original}\n"
        f"[dim]Merged:[/dim]     [bold cyan]{approved}[/bold cyan]\n"
        f"[dim]NAK'd:[/dim]      [red]{rejected}[/red]\n\n"
        f"[dim italic]{signature}[/dim italic]",
        title="[bold yellow]🐧 Final Review Comments 🐧[/bold yellow]",
        box=box.DOUBLE,
        style=style,
    ))
    
    console.print()
    console.print("[dim]Usage: python linus_sort.py [patch1 patch2 ...] or run interactively[/dim]")
    console.print()


if __name__ == "__main__":
    main()
