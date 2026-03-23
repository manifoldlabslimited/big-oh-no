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
from rich.rule import Rule
from .utils import SortInput, ValidationError

console = Console()


def parse_numbers(numbers):
    """Validate and normalize input numbers with Pydantic."""
    try:
        return SortInput(numbers=list(numbers)).numbers
    except ValidationError as e:
        first_error = e.errors()[0]
        location = ".".join(str(part) for part in first_error.get("loc", []))
        message = first_error.get("msg", "Invalid value")
        raise click.BadParameter(f"{location}: {message}", param_hint="numbers")


def show_banner():
    """Display the Big O(No) banner."""
    banner = """
┌───────────────────────────────────────────────────────────────────┐
│██████╗ ██╗ ██████╗      ██████╗ ██╗  ██╗    ███╗   ██╗ ██████╗ ██╗│
│██╔══██╗██║██╔════╝     ██╔═══██╗██║  ██║    ████╗  ██║██╔═══██╗██║│
│██████╔╝██║██║  ███╗    ██║   ██║███████║    ██╔██╗ ██║██║   ██║██║│
│██╔══██╗██║██║   ██║    ██║   ██║██╔══██║    ██║╚██╗██║██║   ██║╚═╝│
│██████╔╝██║╚██████╔╝    ╚██████╔╝██║  ██║    ██║ ╚████║╚██████╔╝██╗│
│╚═════╝ ╚═╝ ╚═════╝      ╚═════╝ ╚═╝  ╚═╝    ╚═╝  ╚═══╝ ╚═════╝ ╚═╝│
│   Utterly Useless Yet Entertaining Sorting Algorithms             │
└───────────────────────────────────────────────────────────────────┘
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
    table.add_row(
        "bogo",
        "🎲 The Gambler",
        "Shuffle repeatedly until sorted",
        "O((n+1)!) expected time",
    )
    table.add_row(
        "schrodinger",
        "🐱 The Quantum Observer",
        "Collapses to least convenient state on observation",
        "O(1) collapse · O(∞) regret",
    )
    table.add_row(
        "urinal",
        "🚽 The Personal Space Enthusiast",
        "Softmax etiquette utility with adjacency aversion dial",
        "O(rounds × n³) time",
    )
    table.add_row(
        "digit",
        "🗂️  The Bucket Bureaucrat",
        "Routes each number to its digit bucket — no comparisons, just classification",
        "O(d × n) time",
    )
    table.add_row(
        "darwin",
        "🧬 The Naturalist",
        "Evolves permutations through selection, crossover, and mutation",
        "O(generations × population × n) time",
    )
    table.add_row(
        "vibe",
        "🫠 The Vibe Checker",
        "Asks an AI to sort by vibes. --pro exec's AI-generated code.",
        "O(vibes)",
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
        big-oh-no bogo 3 2 1
        big-oh-no schrodinger 5 3 1 4
        big-oh-no urinal 8 3 6 1 9 2
        big-oh-no digit 170 45 75 90 2 802 66
        big-oh-no darwin 5 3 1 4 2
        big-oh-no vibe 5 3 1 4 2
        big-oh-no vibe --pro 5 3 1 4 2
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
@click.argument('numbers', nargs=-1, type=int, required=True)
def wait(numbers):
    """
    ⏳ Wait Sort - The most patient sorting algorithm.
    
    Each number spawns a thread that waits for (value × 1) seconds.
    Smaller numbers finish first, resulting in a sorted output.
    
    \b
    Examples:
        big-oh-no wait 5 2 8 1 3
    """
    from . import wait_sort as ws

    nums = parse_numbers(numbers)

    ws.console.print()
    ws.console.print(ws.create_header())
    
    ws.console.print(Panel(
        "[bold]How Wait Sort Works:[/bold]\n\n"
        "• Each number spawns a thread that [cyan]waits[/cyan] for (value) seconds\n"
        "• Smaller numbers finish waiting [green]first[/green]\n"
        "• Numbers are collected in the order they finish\n"
        "• Result: [bold green]Naturally sorted![/bold green]\n\n"
        "[dim]Complexity: O(max(n)) time · O(n) threads · 100% patience required[/dim]",
        title="[bold cyan]💡 Algorithm Explanation[/bold cyan]",
        box=box.ROUNDED,
        padding=(1, 2),
    ))
    
    ws.console.print(f"\n[dim]Numbers:[/dim] [bold cyan]{nums}[/bold cyan]")
    
    sorted_nums, total_time = ws.wait_sort(nums)
    
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


def _stalin_verdict(survivors, original):
    """Return (verdict_text, style) based on survival rate."""
    rate = (len(survivors) / len(original)) * 100
    if rate == 100:
        return "🎖️  Perfect! The list was already in order. No purge needed.", "green"
    if rate >= 70:
        return "📈 Acceptable losses. The party is pleased.", "yellow"
    if rate >= 40:
        return "⚠️  Significant casualties. But order has been achieved.", "yellow"
    return "💀 Brutal. But necessary.", "red"


def _stalin_results(original, survivors, eliminated):
    """Print the results table, comparison visual, and verdict panel."""
    from . import stalin_sort as ss

    ss.console.print()
    ss.console.print(Align.center(ss.create_result_table(original, survivors, eliminated)))
    ss.console.print()
    ss.create_comparison_visual(original, survivors, eliminated)

    verdict, style = _stalin_verdict(survivors, original)

    ss.console.print()
    ss.console.print(Panel(
        f"[bold {style}]{verdict}[/bold {style}]\n\n"
        f"[dim]Original:[/dim]  {original}\n"
        f"[dim]Sorted:[/dim]    [bold cyan]{survivors}[/bold cyan]\n"
        f"[dim]Eliminated:[/dim] [red]{eliminated}[/red]",
        title="[bold yellow]☭ Final Verdict ☭[/bold yellow]",
        box=box.DOUBLE,
        style=style,
    ))
    ss.console.print()


@cli.command()
@click.option('--visualize', '-v', is_flag=True, help='Animated bar chart visualization with sound.')
@click.argument('numbers', nargs=-1, type=int, required=True)
def stalin(visualize, numbers):
    """
    ☭ Stalin Sort - Order through elimination.
    
    Iterates through the list and eliminates any element that is smaller
    than the current maximum. Survivors form a sorted list.
    
    Use --visualize for an animated bar chart with sound.
    
    \b
    Examples:
        big-oh-no stalin 5 1 9 2 8 3 10
        big-oh-no stalin -v 5 1 9 2 8 3 10
    """
    from . import stalin_sort as ss

    nums = parse_numbers(numbers)
    original = nums.copy()

    if visualize:
        from .visualizer import run_visualization
        result = {}
        run_visualization(ss.stalin_sort_viz(nums, result=result), algo_name="☭ Stalin Sort", delay=0.4)
        _stalin_results(original, result["survivors"], result["eliminated"])
        return

    survivors, eliminated = ss.stalin_sort(nums)
    _stalin_results(original, survivors, eliminated)


@cli.command()
@click.argument('numbers', nargs=-1, type=int, required=True)
def linus(numbers):
    """
    🐧 Linus Sort - Code review with maximum hostility.
    
    Each element is reviewed by a simulated Linus Torvalds.
    Elements that break monotonic order get NAK'd with colorful commentary.
    
    \b
    Examples:
        big-oh-no linus 3 1 7 2 9 5 12
    """
    from . import linus_sort as ls

    nums = parse_numbers(numbers)

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
    
    approved, rejected = ls.linus_sort(nums)
    
    ls.console.print()
    ls.console.print(Align.center(ls.create_result_table(original, approved, rejected)))
    ls.console.print()
    ls.create_comparison_visual(original, approved, rejected)
    
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
    
    ls.console.print()
    ls.console.print(Panel(
        f"[bold {style}]{verdict}[/bold {style}]\n\n"
        f"[dim]Submitted:[/dim]  {original}\n"
        f"[dim]Merged:[/dim]     [bold cyan]{approved}[/bold cyan]\n"
        f"[dim]NAK'd:[/dim]      [red]{rejected}[/red]\n\n"
        f"[dim italic]{signature}[/dim italic]",
        title="[bold yellow]🐧 Final Review Comments 🐧[/bold yellow]",
        box=box.DOUBLE,
        style=style,
    ))
    ls.console.print()


@cli.command()
@click.option(
    "--max-attempts",
    default=10000,
    show_default=True,
    type=click.IntRange(min=1),
    help="Maximum number of random shuffles before giving up.",
)
@click.argument('numbers', nargs=-1, type=int, required=True)
def bogo(max_attempts, numbers):
    """
    🎲 Bogo Sort - Shuffle until the universe cooperates.

    Repeatedly shuffles the list until it happens to be sorted.
    Uses a maximum shuffle cap to avoid infinite despair.

    \b
    Examples:
        big-oh-no bogo 3 2 1
        big-oh-no bogo --max-attempts 5000 3 2 1
    """
    from . import bogo_sort as bs

    nums = parse_numbers(numbers)
    original = nums.copy()

    bs.console.print()
    bs.console.print(bs.create_header())

    bs.console.print(Panel(
        "[bold]How Bogo Sort Works:[/bold]\n\n"
        "• Check if the list is sorted\n"
        "• If not, [magenta]shuffle randomly[/magenta]\n"
        "• Repeat until sorted or the attempt limit is hit\n"
        "• Result: [bold green]Occasional success by luck[/bold green]\n\n"
        "[dim]Complexity: O((n+1)!) expected time · O(1) extra space · 100% chaos[/dim]",
        title="[bold cyan]💡 Algorithm Explanation[/bold cyan]",
        box=box.ROUNDED,
        padding=(1, 2),
    ))

    bs.console.print(f"\n[dim]Numbers:[/dim] [bold cyan]{nums}[/bold cyan]")

    sorted_candidate, attempts, elapsed = bs.bogo_sort(nums, max_attempts=max_attempts)

    bs.console.print()
    bs.console.print(Align.center(bs.create_result_table(original, sorted_candidate, attempts, elapsed)))
    bs.console.print()
    bs.console.print(bs.create_result_panel(original, sorted_candidate, attempts, elapsed))
    bs.console.print()


@cli.command()
@click.option(
    "--meanness",
    default=0.5,
    show_default=True,
    type=click.FloatRange(min=0.0, max=1.0),
    help="How likely the universe is to choose an inconvenient collapse (0.0=kind, 1.0=spiteful).",
)
@click.argument('numbers', nargs=-1, type=int, required=True)
def schrodinger(meanness, numbers):
    """
    🐱 Schrödinger Sort - Sorted and unsorted, until you look.

    The list exists in quantum superposition until observed. On observation
    the wavefunction collapses into whichever state is least convenient.

    \b
    Examples:
        big-oh-no schrodinger 5 3 1 4
        big-oh-no schrodinger --meanness 0.8 5 3 1 4
        big-oh-no schrodinger 1 2 3
    """
    from . import schrodinger_sort as sch

    nums = parse_numbers(numbers)
    original = nums.copy()

    result, collapsed_to_sorted, comment = sch.schrodinger_sort(nums, meanness=meanness)

    sch.console.print()
    sch.console.print(sch.create_result_panel(original, result, collapsed_to_sorted, comment))
    sch.console.print()


@cli.command()
@click.option(
    "--max-rounds",
    default=200,
    show_default=True,
    type=click.IntRange(min=1),
    help="Maximum rounds before giving up (cycle detection usually kicks in first).",
)
@click.option(
    "--awkwardness",
    default=0.5,
    show_default=True,
    type=click.FloatRange(min=0.0, max=1.0),
    help="Neighbour discomfort 0–1. 0.0: indifferent to neighbours. 1.0: maximise distance from everyone.",
)
@click.argument('numbers', nargs=-1, type=int, required=True)
def urinal(max_rounds, awkwardness, numbers):
    """
    🚽 Urinal Sort - Sorting by restroom etiquette. Correctness not guaranteed.

    Numbers enter in list order. Each one picks the least exposed stall.
    Read stalls left to right for the new order. Repeat until sorted or stuck.

    \b
    Examples:
        big-oh-no urinal 1 3 2
        big-oh-no urinal --awkwardness 0.2 8 3 6 1 9 2
        big-oh-no urinal 8 3 6 1 9 2
        big-oh-no urinal 3 2 1
    """
    from . import urinal_sort as us

    nums = parse_numbers(numbers)
    original = nums.copy()

    result, rounds_taken, round_logs, did_sort = us.urinal_sort(
        nums,
        max_rounds=max_rounds,
        awkwardness=awkwardness,
    )

    us.console.print()
    us.console.print(Align.center(
        us.create_result_table(
            original,
            result,
            rounds_taken,
            round_logs,
            did_sort,
            awkwardness,
        )
    ))
    us.console.print()
    us.console.print(us.create_result_panel(original, result, rounds_taken, did_sort))
    us.console.print()


@cli.command()
@click.argument('numbers', nargs=-1, type=int, required=True)
def digit(numbers):
    """
    🗂️  Digit Sort - The Bucket Bureaucrat. No comparisons. Ever.

    Each number is routed to its bucket based on its current digit —
    no value judgements, no comparisons. Just process, file, repeat.

    \b
    Examples:
        big-oh-no digit 170 45 75 90 2 802 66
        big-oh-no digit 3 1 4 1 5 9 2 6
    """
    import random
    from . import digit_sort as ds

    nums = parse_numbers(numbers)
    original = nums.copy()

    ds.console.print()
    ds.console.print(ds.create_header())
    ds.console.print()
    ds.console.print(Panel(
        "• Route each number to a [blue]bucket (0–9)[/blue] based on its current digit\n"
        "• Collect buckets in order, repeat for each digit position\n"
        "• [bold red]No comparisons between values. Ever.[/bold red]\n\n"
        "[dim]O(d × n) time · 0 comparisons · ∞ paperwork[/dim]",
        title="[bold cyan]🗂️  How It Works[/bold cyan]",
        box=box.ROUNDED,
        padding=(0, 2),
    ))

    # digit_sort now handles animation internally
    sorted_nums, passes = ds.digit_sort(nums)

    ds.console.print(Rule("[bold green]✨ Filing Complete[/bold green]", style="green"))
    ds.console.print()

    ds.console.print(Align.center(ds.create_result_table(original, sorted_nums, passes)))
    ds.console.print()
    ds.create_comparison_bars(original, sorted_nums)

    completion = random.choice(ds.COMPLETION_REMARKS)
    ds.console.print()
    ds.console.print(Panel(
        f"[bold green]✅ {len(original)} items filed in {len(passes)} pass(es). "
        f"0 comparisons.[/bold green]\n\n"
        f"[dim]Original:[/dim] {original}\n"
        f"[dim]Sorted:[/dim]   [bold cyan]{sorted_nums}[/bold cyan]\n\n"
        f"[dim italic]{completion}[/dim italic]",
        title="[bold yellow]🗂️  Processing Complete[/bold yellow]",
        box=box.DOUBLE,
        style="green",
    ))
    ds.console.print()


@cli.command()
@click.option('--visualize', '-v', is_flag=True, help='Animated bar chart visualization with sound.')
@click.option(
    "--max-generations",
    default=500,
    show_default=True,
    type=click.IntRange(min=1),
    help="Maximum generations before the species goes extinct.",
)
@click.option(
    "--population-size",
    default=50,
    show_default=True,
    type=click.IntRange(min=2),
    help="Number of individuals in each generation.",
)
@click.option(
    "--mutation-rate",
    default=0.2,
    show_default=True,
    type=click.FloatRange(min=0.0, max=1.0),
    help="Probability of mutating an individual (0.0=stable, 1.0=chaos).",
)
@click.option(
    "--crossover-rate",
    default=0.7,
    show_default=True,
    type=click.FloatRange(min=0.0, max=1.0),
    help="Probability of crossover between parents (0.0=clones, 1.0=always mix).",
)
@click.argument('numbers', nargs=-1, type=int, required=True)
def darwin(visualize, max_generations, population_size, mutation_rate, crossover_rate, numbers):
    """
    🧬 Darwin Sort - Survival of the fittest permutation.

    Charles Darwin watches your numbers compete for survival across
    generations. A population of candidate permutations evolves through
    selection, crossover, and mutation until the sorted order emerges
    — or the species goes extinct trying.

    Use --visualize for an animated bar chart with sound.

    \b
    Examples:
        big-oh-no darwin 5 3 1 4 2
        big-oh-no darwin -v 5 3 1 4 2
        big-oh-no darwin --max-generations 200 9 1 8 2 7
        big-oh-no darwin --population-size 100 --mutation-rate 0.5 5 3 1 4 2
    """
    from . import darwin_sort as ds

    nums = parse_numbers(numbers)
    original = nums.copy()

    if visualize:
        from .visualizer import run_visualization
        result = {}
        run_visualization(
            ds.darwin_sort_viz(
                nums, max_generations=max_generations,
                population_size=population_size,
                crossover_prob=crossover_rate,
                mutation_prob=mutation_rate,
                result=result,
            ),
            algo_name="🧬 Darwin Sort",
            delay=0.05,
        )
        r = result
        ds.console.print()
        ds.console.print(Align.center(ds.create_result_table(
            original, r["sorted"], r["generations"], r["elapsed"], r["converged"],
        )))
        ds.console.print()
        ds.console.print(ds.create_result_panel(
            original, r["sorted"], r["generations"], r["elapsed"], r["converged"],
        ))
        ds.console.print()
        return

    result, generations, elapsed, converged, logbook = ds.darwin_sort(
        nums,
        max_generations=max_generations,
        population_size=population_size,
        crossover_prob=crossover_rate,
        mutation_prob=mutation_rate,
    )

    ds.console.print()
    ds.console.print(Align.center(ds.create_result_table(
        original, result, generations, elapsed, converged, logbook,
    )))
    ds.console.print()
    ds.console.print(ds.create_result_panel(original, result, generations, elapsed, converged))
    ds.console.print()

@cli.command()
@click.option("--pro", is_flag=True, default=False, help="Ask the AI to write sorting code, then exec it. Peak vibe coding.")
@click.argument("numbers", nargs=-1, required=True, type=int)
def vibe(pro, numbers):
    """
    🫠 Vibe Sort - Why think when you can just feel it?

    Sends the list to an AI agent and asks it to sort by vibes.
    The algorithm doesn't compare. It doesn't compute. It just feels
    the correct order and ships it.

    No API key? No vibes. Shuffles randomly and calls it intuition.

    Use --pro for a coding agent that writes and runs a sorting function. Like a pro.

    \b
    Examples:
        big-oh-no vibe 5 3 1 4 2
        big-oh-no vibe --pro 5 3 1 4 2
    """
    import random
    from rich.syntax import Syntax
    from . import vibe_sort as vs

    nums = parse_numbers(numbers)
    original = nums.copy()

    vs.console.print()
    vs.console.print(vs.create_header())

    # ── Interactive model selection ──────────────────────────────────────
    MODEL_CHOICES = {
        "1": ("openai:gpt-5-mini", "GPT-5 Mini"),
        "2": ("anthropic:claude-sonnet-4-6", "Claude Sonnet 4.6"),
        "3": ("anthropic:claude-sonnet-4-5", "Claude Sonnet 4.5"),
        "4": (None, "No model — just vibes"),
    }

    vs.console.print(Panel(
        "\n".join(
            f"  [bold cyan]{k}[/bold cyan]) {label}" for k, (_, label) in MODEL_CHOICES.items()
        ),
        title="[bold yellow]🫠 Pick your vibe source (or don't)[/bold yellow]",
        box=box.ROUNDED,
        padding=(1, 2),
    ))

    choice = click.prompt("Choose", type=click.Choice(list(MODEL_CHOICES)), default="4")
    model, label = MODEL_CHOICES[choice]

    api_key = None
    if model is not None:
        api_key = click.prompt("API key", hide_input=True)

    mode_label = "PRO (coding agent)" if pro and model is not None else label
    vs.console.print()
    vs.console.print(Panel(
        "[bold]How Vibe Sort Works:[/bold]\n\n"
        + (
            "• A [bold red]coding agent[/bold red] writes a sorting function\n"
            "• Then executes it. Like a pro.\n"
            "• [magenta]The generated code gets displayed. Don't read it.[/magenta]\n"
            "• If it works, it was meant to be.\n\n"
            if pro and model is not None else
            "• Send the list to an agent. Ask it to sort by vibes.\n"
            "• The agent doesn't compare. It [magenta]feels[/magenta] the order.\n"
            "• Ship it before anyone applies logic.\n\n"
        )
        + f"[dim]Model: {mode_label} · Complexity: O(vibes)[/dim]",
        title="[bold cyan]💡 Algorithm Explanation[/bold cyan]",
        box=box.ROUNDED,
        padding=(1, 2),
    ))

    vs.console.print(f"\n[dim]Numbers:[/dim] [bold cyan]{nums}[/bold cyan]")
    vs.console.print(f"[dim italic]\"{random.choice(vs.VIBE_REMARKS)}\"[/dim italic]\n")

    vs.animate_vibe(is_offline=api_key is None, is_pro=pro and api_key is not None)

    result, explanation, elapsed, model_used, generated_code = vs.vibe_sort(
        nums,
        model=model or vs.DEFAULT_MODEL,
        api_key=api_key,
        pro=pro and api_key is not None,
    )

    if model_used == "offline-vibes" and model is not None:
        vs.console.print("[bold yellow]⚠️  AI call failed. Falling back to unguided vibes.[/bold yellow]\n")

    if generated_code is not None:
        vs.console.print(Panel(
            Syntax(generated_code, "python", theme="monokai", line_numbers=True),
            title="[bold red]🔥 AI-Generated Code (written and executed by a coding agent)[/bold red]",
            box=box.DOUBLE,
            style="red",
        ))
        vs.console.print()

    vs.console.print()
    vs.console.print(Align.center(vs.create_result_table(
        original, result, explanation, elapsed, model_used, generated_code,
    )))
    vs.console.print()
    vs.console.print(vs.create_result_panel(original, result, explanation, elapsed))
    vs.console.print()



def main():
    """Entry point for the CLI."""
    cli()


if __name__ == "__main__":
    main()
