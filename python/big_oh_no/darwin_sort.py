#!/usr/bin/env python3
"""
Darwin Sort — Survival of the fittest permutation.

Charles Darwin watches your numbers compete for survival across generations.
A population of candidate permutations evolves through selection, crossover,
and mutation until natural selection discovers the sorted order — or the
species goes extinct trying.
"""

import random
import time

import numpy as np
from deap import algorithms, base, creator, tools
from pydantic import BaseModel, Field
from rich import box
from rich.align import Align
from rich.panel import Panel
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn
from rich.rule import Rule
from rich.table import Table

from .utils import console, make_sort_header

# ── Default GA hyper-parameters ──────────────────────────────────────────────
DEFAULT_POPULATION_SIZE = 50
DEFAULT_CROSSOVER_PROB = 0.7
DEFAULT_MUTATION_PROB = 0.2
DEFAULT_TOURNAMENT_SIZE = 3

FRAME_DELAY = 0.03


# ── Pydantic parameter validation ───────────────────────────────────────────
class _DarwinSortParams(BaseModel):
    max_generations: int = Field(ge=1)
    population_size: int = Field(ge=2)
    crossover_prob: float = Field(ge=0.0, le=1.0)
    mutation_prob: float = Field(ge=0.0, le=1.0)


# ── Flavor text ──────────────────────────────────────────────────────────────
GENERATION_REMARKS = [
    "The weak perish. The sorted endure.",
    "Natural selection is a patient teacher.",
    "Only the fittest permutations survive to breed.",
    "Darwin scribbles notes in his journal.",
    "Mutations ripple through the gene pool.",
    "The Galápagos finches would be proud.",
    "Crossover produces promising offspring.",
    "The unfit are culled. Nature is indifferent.",
    "Adaptation in progress. Do not disturb.",
    "Survival pressure intensifies.",
]

CONVERGENCE_REMARKS = [
    "After countless generations, order emerges from chaos. Darwin nods approvingly.",
    "Natural selection has spoken. The sorted survive.",
    "Evolution finds a way. It always does. Eventually.",
    "The fittest permutation stands alone. Sorted.",
    "Charles Darwin wipes a tear. Beautiful.",
]

EXTINCTION_REMARKS = [
    "The gene pool has been exhausted. Darwin sighs.",
    "Evolution tried its best. Its best wasn't enough.",
    "Not every species makes it. Neither did this list.",
    "The generation budget ran dry. Some things aren't meant to be sorted.",
    "Darwin closes his notebook. 'Perhaps next epoch,' he mutters.",
]

# ── DEAP type registration (guarded against repeated imports in tests) ───────
if not hasattr(creator, "FitnessEvolution"):
    creator.create("FitnessEvolution", base.Fitness, weights=(1.0,))
if not hasattr(creator, "IndividualEvolution"):
    creator.create("IndividualEvolution", list, fitness=creator.FitnessEvolution)


# ── Pure helpers ──────────────────────────────────────────────────────────────

def fitness(values):
    """Fraction of adjacent pairs in order. Returns a DEAP-style 1-tuple."""
    n = len(values)
    if n <= 1:
        return (1.0,)
    correct = sum(1 for i in range(n - 1) if values[i] <= values[i + 1])
    return (correct / (n - 1),)


def _score(result):
    """Convenience: unpack the 1-tuple fitness into a plain float."""
    return fitness(result)[0]


def _decode(individual, numbers):
    """Translate an index-permutation individual back to actual values."""
    return [numbers[i] for i in individual]


def _build_toolbox(numbers):
    """Return a fresh DEAP Toolbox wired up for the given input list."""
    indices = list(range(len(numbers)))

    def evaluate(individual):
        return fitness(_decode(individual, numbers))

    tb = base.Toolbox()
    tb.register("indices", random.sample, indices, len(indices))
    tb.register("individual", tools.initIterate, creator.IndividualEvolution, tb.indices)
    tb.register("population", tools.initRepeat, list, tb.individual)
    tb.register("evaluate", evaluate)
    tb.register("mate", tools.cxOrdered)
    tb.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
    tb.register("select", tools.selTournament, tournsize=DEFAULT_TOURNAMENT_SIZE)
    return tb


# ── Core algorithm (pure logic — no animation) ───────────────────────────────

def _evolve(numbers, max_generations, population_size, crossover_prob, mutation_prob):
    """
    Run the GA and return (result, generation, elapsed, converged, hof, logbook).

    This is the pure algorithm with zero UI side-effects.
    """
    toolbox = _build_toolbox(numbers)
    pop = toolbox.population(n=population_size)

    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values[0])
    stats.register("avg", np.mean)
    stats.register("max", np.max)
    stats.register("min", np.min)

    # Evaluate initial population so eaSimple doesn't double-evaluate
    for ind in pop:
        ind.fitness.values = toolbox.evaluate(ind)

    started = time.time()
    pop, logbook = algorithms.eaSimple(
        pop, toolbox,
        cxpb=crossover_prob,
        mutpb=mutation_prob,
        ngen=max_generations,
        stats=stats,
        halloffame=hof,
        verbose=False,
    )
    elapsed = time.time() - started

    best_fitness = hof[0].fitness.values[0]
    converged = best_fitness == 1.0
    result = _decode(hof[0], numbers)

    # Find the generation convergence happened
    max_fits = logbook.select("max")
    generation = next((i for i, f in enumerate(max_fits) if f == 1.0), max_generations)

    return result, generation, elapsed, converged, hof, logbook


# ── Public entry point (algorithm + animation) ───────────────────────────────

def darwin_sort(
    numbers,
    max_generations=500,
    population_size=DEFAULT_POPULATION_SIZE,
    crossover_prob=DEFAULT_CROSSOVER_PROB,
    mutation_prob=DEFAULT_MUTATION_PROB,
):
    """
    Sort *numbers* using a genetic algorithm powered by DEAP's eaSimple.

    Returns (sorted_list, generations_taken, elapsed_seconds, converged, logbook).
    """
    _DarwinSortParams(
        max_generations=max_generations,
        population_size=population_size,
        crossover_prob=crossover_prob,
        mutation_prob=mutation_prob,
    )

    if len(numbers) <= 1:
        return numbers.copy(), 0, 0.0, True, tools.Logbook()

    # Run the actual GA
    result, generation, elapsed, converged, hof, logbook = _evolve(
        numbers, max_generations, population_size, crossover_prob, mutation_prob,
    )

    # Animate the results
    _animate(numbers, result, generation, elapsed, converged, hof, logbook,
             max_generations, population_size, crossover_prob, mutation_prob)

    return result, generation, elapsed, converged, logbook


# ── Animation ─────────────────────────────────────────────────────────────────


def _animate(numbers, result, generation, elapsed, converged, hof, logbook,
             max_generations, population_size, crossover_prob, mutation_prob):
    """Render the full Darwin Sort CLI experience from a completed logbook."""
    best_fitness = _score(result)
    n_pairs = len(numbers) - 1
    gen0 = logbook[0]

    # Phase 1: Header + config
    console.print()
    console.print(create_header())
    console.print()
    console.print(Align.center(_create_config_table(
        numbers, max_generations, population_size, crossover_prob, mutation_prob,
    )))
    console.print()

    # Phase 2: Initial population stats from logbook
    console.print(Rule("[bold green]🌍 Populating the Galápagos[/bold green]", style="green"))
    console.print()

    decoded_best = _decode(hof[0], numbers)
    best_fit = hof[0].fitness.values[0]
    time.sleep(0.25)
    console.print(
        f"  [dim]Best specimen:[/dim] [bold]{decoded_best}[/bold]  "
        f"{_fitness_bar(best_fit)} [cyan]{best_fit:.0%}[/cyan]"
    )
    console.print()
    console.print(
        f"  [dim]Population:[/dim] [cyan]{population_size}[/cyan] individuals  "
        f"[dim]Avg fitness:[/dim] [yellow]{gen0['avg']:.0%}[/yellow]  "
        f"[dim]Best:[/dim] [green]{gen0['max']:.0%}[/green]"
    )
    console.print(f"  [dim]Darwin:[/dim] [italic]\"Interesting specimens. Let natural selection begin.\"[/italic]")
    console.print()
    time.sleep(0.3)

    # Phase 3: Replay evolution from logbook
    console.print(Rule("[bold green]🧬 Natural Selection[/bold green]", style="green"))
    console.print()

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=40, style="green", complete_style="bright_green", finished_style="bright_green"),
        TextColumn("[cyan]{task.completed}[/cyan]/[dim]{task.total}[/dim] gens"),
        console=console,
        expand=False,
    ) as progress:
        task_id = progress.add_task("[green]🧬 Evolving…[/green]", total=generation or 1)

        for rec in logbook:
            gen = rec["gen"]
            if gen == 0:
                continue

            show_detail = gen <= 20 or gen % 25 == 0 or rec["max"] == 1.0
            if show_detail:
                correct_pairs = round(rec["max"] * n_pairs)
                time.sleep(FRAME_DELAY)
                progress.update(
                    task_id,
                    completed=min(gen, generation),
                    description=(
                        f"[green]Gen {gen}:[/green] "
                        f"[dim]({correct_pairs}/{n_pairs} pairs · "
                        f"avg {rec['avg']:.0%})[/dim] "
                        f"[dim italic]{random.choice(GENERATION_REMARKS)}[/dim italic]"
                    ),
                )
            else:
                progress.update(task_id, completed=min(gen, generation))

            if rec["max"] == 1.0:
                progress.update(
                    task_id, completed=generation,
                    description="[bright_green]✅ Perfect fitness — the sorted survive![/bright_green]",
                )
                break
        else:
            progress.update(
                task_id, completed=generation,
                description=(
                    "[yellow]⚠️ Species went extinct[/yellow] "
                    f"[dim](best fitness: {best_fitness:.0%})[/dim]"
                ),
            )

    console.print()

    # Phase 4: Darwin's verdict
    if converged:
        console.print(Rule("[bold bright_green]✨ Evolution Converged[/bold bright_green]", style="bright_green"))
        console.print()
        console.print(f"  [dim italic]\"{random.choice(CONVERGENCE_REMARKS)}\"[/dim italic]")
    else:
        console.print(Rule("[bold yellow]💀 Extinction Event[/bold yellow]", style="yellow"))
        console.print()
        console.print(f"  [dim italic]\"{random.choice(EXTINCTION_REMARKS)}\"[/dim italic]")

    console.print()



# ── Rich UI helpers ───────────────────────────────────────────────────────────

def create_header():
    return make_sort_header("🧬", "darwin", "Survival of the fittest permutation", "green")


def _fitness_bar(fit):
    """Render a visual fitness meter."""
    width = 15
    filled = int(width * fit)
    empty = width - filled
    if fit >= 0.9:
        col = "bright_green"
    elif fit >= 0.6:
        col = "yellow"
    else:
        col = "red"
    return f"[{col}]{'█' * filled}[/{col}][dim]{'░' * empty}[/dim]"


def _create_config_table(numbers, max_generations, population_size, crossover_prob, mutation_prob):
    table = Table(
        title="🔬 Darwin's Laboratory",
        box=box.ROUNDED,
        title_style="bold green",
        show_header=True,
        header_style="bold cyan",
    )
    table.add_column("Parameter", style="dim")
    table.add_column("Value", style="green")

    table.add_row("Specimens", f"[bold]{numbers}[/bold]")
    table.add_row("Population size", f"[cyan]{population_size}[/cyan] individuals")
    table.add_row("Max generations", f"[magenta]{max_generations}[/magenta]")
    table.add_row("Crossover rate", f"[yellow]{crossover_prob:.0%}[/yellow]")
    table.add_row("Mutation rate", f"[yellow]{mutation_prob:.0%}[/yellow]")
    table.add_row("Selection", f"[dim]Tournament (k={DEFAULT_TOURNAMENT_SIZE})[/dim]")
    table.add_row("Strategy", "[dim]Elitism (HallOfFame) + order crossover[/dim]")
    return table


def create_result_table(original, result, generations, elapsed, converged, logbook=None):
    """Summary table for the CLI output."""
    best_fitness = _score(result)

    table = Table(
        title="📊 Darwin's Field Notes",
        box=box.ROUNDED,
        title_style="bold green",
        show_header=True,
        header_style="bold cyan",
    )
    table.add_column("Observation", style="dim")
    table.add_column("Value", style="cyan")

    n_pairs = max(len(result) - 1, 0)
    correct = round(best_fitness * n_pairs) if n_pairs else 0

    table.add_row("Original species", f"{original}")
    table.add_row("Evolved form", f"[bold]{result}[/bold]")
    table.add_row("Generations", f"[magenta]{generations}[/magenta]")
    table.add_row("Evolution time", f"[green]{elapsed:.4f}s[/green]")
    table.add_row(
        "Final fitness",
        f"{_fitness_bar(best_fitness)} [yellow]{correct}/{n_pairs}[/yellow] pairs",
    )

    if logbook and len(logbook) > 0:
        last = logbook[-1]
        table.add_row(
            "Final population",
            f"[dim]avg {last['avg']:.0%} · best {last['max']:.0%} · worst {last['min']:.0%}[/dim]",
        )
        total_evals = sum(rec["nevals"] for rec in logbook)
        table.add_row("Total evaluations", f"[dim]{total_evals}[/dim]")

    table.add_row(
        "Outcome",
        "[bright_green]Sorted — species thrives[/bright_green]"
        if converged
        else "[red]Unsorted — species extinct[/red]",
    )
    return table


def create_result_panel(original, result, generations, elapsed, converged):
    """Final summary panel for the CLI."""
    best_fitness = _score(result)
    n_pairs = max(len(result) - 1, 0)
    correct = round(best_fitness * n_pairs) if n_pairs else 0

    if converged:
        message = (
            "[bold bright_green]Natural selection found the sorted order.[/bold bright_green]\n\n"
            f"[dim]Original:[/dim]    {original}\n"
            f"[dim]Sorted:[/dim]      [bold cyan]{result}[/bold cyan]\n"
            f"[dim]Generations:[/dim] {generations}\n"
            f"[dim]Time:[/dim]        {elapsed:.4f}s"
        )
        title = "[bold yellow]🧬 Darwin Approves[/bold yellow]"
        style = "bright_green"
    else:
        message = (
            "[bold yellow]The gene pool has been exhausted. "
            "Darwin closes his notebook.[/bold yellow]\n\n"
            f"[dim]Original:[/dim]    {original}\n"
            f"[dim]Best:[/dim]        [bold cyan]{result}[/bold cyan]\n"
            f"[dim]Fitness:[/dim]     {correct}/{n_pairs} pairs in order\n"
            f"[dim]Generations:[/dim] {generations}\n"
            f"[dim]Time:[/dim]        {elapsed:.4f}s"
        )
        title = "[bold yellow]💀 Extinction Event[/bold yellow]"
        style = "yellow"

    return Panel(message, title=title, box=box.DOUBLE, style=style)
