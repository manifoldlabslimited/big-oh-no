#!/usr/bin/env python3
"""
Evolution Sort - Sorting as natural selection.

Treats sorting as an optimisation problem and solves it with a genetic algorithm.
A population of candidate permutations evolves through selection, crossover, and
mutation until natural selection discovers the sorted order — or gives up.
"""

import random
import time

from deap import algorithms, base, creator, tools
from rich import box
from rich.align import Align
from rich.panel import Panel
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn
from rich.rule import Rule
from rich.table import Table

from .utils import console, make_sort_header

# ── GA hyper-parameters (hidden from CLI; they are fun internals) ────────────
POPULATION_SIZE = 50
CROSSOVER_PROB = 0.7
MUTATION_PROB = 0.2
TOURNAMENT_SIZE = 3

FRAME_DELAY = 0.03  # seconds between generation renders

# ── DEAP type registration (guarded against repeated imports in tests) ────────
if not hasattr(creator, "FitnessEvolution"):
    creator.create("FitnessEvolution", base.Fitness, weights=(1.0,))
if not hasattr(creator, "IndividualEvolution"):
    creator.create("IndividualEvolution", list, fitness=creator.FitnessEvolution)


# ── Helpers ───────────────────────────────────────────────────────────────────

def create_header():
    return make_sort_header("🧬", "evolution", "Survival of the most-sorted", "green")


def fitness(values):
    """
    Score a permutation of *values* by the fraction of adjacent pairs in order.

    This is the public fitness function that accepts actual values (not indices).
    It is also used directly in tests.

    Returns a 1-tuple to match DEAP convention.
    """
    n = len(values)
    if n <= 1:
        return (1.0,)
    correct = sum(1 for i in range(n - 1) if values[i] <= values[i + 1])
    return (correct / (n - 1),)


def _make_evaluate(numbers):
    """Return a DEAP-compatible evaluate function closed over *numbers*.

    Individuals are permutations of *indices* (not values), so the evaluate
    function must decode them before scoring.
    """
    def evaluate(individual):
        decoded = [numbers[i] for i in individual]
        return fitness(decoded)
    return evaluate


def is_sorted(values):
    return all(values[i] <= values[i + 1] for i in range(len(values) - 1))


def _build_toolbox(numbers):
    """Return a fresh DEAP Toolbox wired up for the given input list."""
    indices = list(range(len(numbers)))

    toolbox = base.Toolbox()
    toolbox.register("indices", random.sample, indices, len(indices))
    toolbox.register(
        "individual",
        tools.initIterate,
        creator.IndividualEvolution,
        toolbox.indices,
    )
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", _make_evaluate(numbers))
    toolbox.register("mate", tools.cxOrdered)
    toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
    toolbox.register("select", tools.selTournament, tournsize=TOURNAMENT_SIZE)
    return toolbox


def _decode(individual, numbers):
    """Translate an index-permutation individual back to actual values."""
    return [numbers[i] for i in individual]


# ── Core algorithm ────────────────────────────────────────────────────────────

def evolution_sort(numbers, max_generations=500):
    """
    Sort *numbers* using a genetic algorithm.

    Returns (sorted_list, generations_taken, elapsed_seconds, converged).
    When *converged* is False the best individual found is returned instead.
    """
    if len(numbers) <= 1:
        return numbers.copy(), 0, 0.0, True

    toolbox = _build_toolbox(numbers)
    pop = toolbox.population(n=POPULATION_SIZE)

    started = time.time()
    best_individual = None
    best_fitness = -1.0
    generation = 0

    hype_lines = [
        "[green]🧬 Mutations firing…[/green]",
        "[green]🧬 Crossing over chromosomes…[/green]",
        "[green]🧬 Natural selection in progress…[/green]",
        "[green]🧬 Darwin would be proud (maybe)[/green]",
        "[green]🧬 Survival of the most-sorted…[/green]",
    ]

    console.print()
    console.print(create_header())
    console.print()
    console.print(Align.center(_create_config_table(numbers, max_generations)))
    console.print()
    console.print(Rule("[bold green]🧬 Initiating Evolution[/bold green]", style="green"))

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=40, style="green", complete_style="bright_green", finished_style="bright_green"),
        TextColumn("[cyan]{task.completed}[/cyan]/[dim]{task.total}[/dim] gens"),
        console=console,
        expand=False,
    ) as progress:
        task_id = progress.add_task(
            "[green]🧬 Evolving population…[/green]",
            total=max_generations,
        )

        # Evaluate initial population
        fitnesses = map(toolbox.evaluate, pop)
        for ind, fit in zip(pop, fitnesses):
            ind.fitness.values = fit

        for generation in range(1, max_generations + 1):
            # ── Selection ─────────────────────────────────────────
            offspring = toolbox.select(pop, len(pop))
            offspring = list(map(toolbox.clone, offspring))

            # ── Crossover ─────────────────────────────────────────
            for child1, child2 in zip(offspring[::2], offspring[1::2]):
                if random.random() < CROSSOVER_PROB:
                    toolbox.mate(child1, child2)
                    del child1.fitness.values
                    del child2.fitness.values

            # ── Mutation ──────────────────────────────────────────
            for mutant in offspring:
                if random.random() < MUTATION_PROB:
                    toolbox.mutate(mutant)
                    del mutant.fitness.values

            # ── Re-evaluate stale individuals ─────────────────────
            invalid = [ind for ind in offspring if not ind.fitness.valid]
            fitnesses = map(toolbox.evaluate, invalid)
            for ind, fit in zip(invalid, fitnesses):
                ind.fitness.values = fit

            # ── Elitism: carry the best forward, replacing the worst ──
            elite = tools.selBest(pop, 1)
            worst_idx = min(range(len(offspring)), key=lambda i: offspring[i].fitness.values[0])
            offspring[worst_idx] = toolbox.clone(elite[0])

            pop[:] = offspring

            # ── Track the global best ─────────────────────────────
            current_best = tools.selBest(pop, 1)[0]
            current_fitness = current_best.fitness.values[0]

            if current_fitness > best_fitness:
                best_fitness = current_fitness
                best_individual = toolbox.clone(current_best)

            # ── Render progress ───────────────────────────────────
            hype = hype_lines[generation % len(hype_lines)]
            decoded = _decode(current_best, numbers)
            n_pairs = len(numbers) - 1
            correct_pairs = round(current_fitness * n_pairs)

            if generation <= 20 or generation % 25 == 0 or current_fitness == 1.0:
                time.sleep(FRAME_DELAY)
                progress.update(
                    task_id,
                    completed=generation,
                    description=(
                        f"[green]Gen {generation}:[/green] [bold]{decoded}[/bold] "
                        f"[dim]({correct_pairs}/{n_pairs} pairs)[/dim] {hype}"
                    ),
                )
            else:
                progress.update(task_id, completed=generation)

            # ── Termination check ─────────────────────────────────
            if current_fitness == 1.0:
                progress.update(
                    task_id,
                    completed=generation,
                    description="[bright_green]✅ Perfect fitness achieved — evolution wins![/bright_green]",
                )
                break

        else:
            progress.update(
                task_id,
                completed=max_generations,
                description=(
                    "[yellow]⚠️ Max generations reached[/yellow] "
                    f"[dim](best fitness: {best_fitness:.2%})[/dim]"
                ),
            )

    elapsed = time.time() - started
    converged = best_fitness == 1.0
    result = _decode(best_individual, numbers)

    console.print()
    if converged:
        console.print(Rule("[bold bright_green]✨ Evolution Converged[/bold bright_green]", style="bright_green"))
    else:
        console.print(Rule("[bold yellow]⚠️ Generation Budget Exhausted[/bold yellow]", style="yellow"))

    return result, generation, elapsed, converged


# ── Rich UI helpers ───────────────────────────────────────────────────────────

def _create_config_table(numbers, max_generations):
    table = Table(
        title="🔬 Evolution Parameters",
        box=box.ROUNDED,
        title_style="bold green",
        show_header=True,
        header_style="bold cyan",
    )
    table.add_column("Parameter", style="dim")
    table.add_column("Value", style="green")

    table.add_row("Numbers to sort", f"[bold]{numbers}[/bold]")
    table.add_row("Population size", f"[cyan]{POPULATION_SIZE}[/cyan] individuals")
    table.add_row("Max generations", f"[magenta]{max_generations}[/magenta]")
    table.add_row("Crossover probability", f"[yellow]{CROSSOVER_PROB:.0%}[/yellow]")
    table.add_row("Mutation probability", f"[yellow]{MUTATION_PROB:.0%}[/yellow]")
    return table


def create_result_table(original, result, generations, elapsed, converged):
    """Summary table for the CLI output."""
    n = len(result)
    correct = sum(1 for i in range(n - 1) if result[i] <= result[i + 1])
    max_pairs = max(n - 1, 0)

    table = Table(
        title="📊 Evolution Sort Report",
        box=box.ROUNDED,
        title_style="bold green",
        show_header=True,
        header_style="bold cyan",
    )
    table.add_column("Property", style="dim")
    table.add_column("Value", style="cyan")

    table.add_row("Original", f"{original}")
    table.add_row("Result", f"[bold]{result}[/bold]")
    table.add_row("Generations", f"[magenta]{generations}[/magenta]")
    table.add_row("Elapsed", f"[green]{elapsed:.4f}s[/green]")
    table.add_row(
        "Order meter",
        f"[yellow]{correct}/{max_pairs}[/yellow] adjacent pairs in order",
    )
    table.add_row("Sorted?", "[bright_green]Yes[/bright_green]" if converged else "[red]No[/red]")
    return table


def create_result_panel(original, result, generations, elapsed, converged):
    """Final summary panel for the CLI."""
    if converged:
        message = (
            "[bold bright_green]Natural selection found the sorted order.[/bold bright_green]\n\n"
            f"[dim]Original:[/dim]    {original}\n"
            f"[dim]Sorted:[/dim]      [bold cyan]{result}[/bold cyan]\n"
            f"[dim]Generations:[/dim] {generations}\n"
            f"[dim]Time:[/dim]        {elapsed:.4f}s"
        )
        title = "[bold yellow]🎉 Evolution Wins[/bold yellow]"
        style = "bright_green"
    else:
        n = len(result)
        correct = sum(1 for i in range(n - 1) if result[i] <= result[i + 1])
        max_pairs = max(n - 1, 0)
        message = (
            "[bold yellow]Evolution ran out of generations. The fittest survived anyway.[/bold yellow]\n\n"
            f"[dim]Original:[/dim]    {original}\n"
            f"[dim]Best:[/dim]        [bold cyan]{result}[/bold cyan]\n"
            f"[dim]Fitness:[/dim]     {correct}/{max_pairs} pairs in order\n"
            f"[dim]Generations:[/dim] {generations}\n"
            f"[dim]Time:[/dim]        {elapsed:.4f}s"
        )
        title = "[bold yellow]🧬 Gene Pool Exhausted[/bold yellow]"
        style = "yellow"

    return Panel(message, title=title, box=box.DOUBLE, style=style)
