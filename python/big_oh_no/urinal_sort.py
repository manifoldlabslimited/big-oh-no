#!/usr/bin/env python3
"""
Urinal Sort — The values ARE the people. They sort themselves, reluctantly.

Inspired by the unwritten rules of restroom etiquette: stay as far from others
as possible, avoid being flanked, and favour a wall when the room is open. No
one co-ordinates. Each person just picks the stall that feels least exposed, and
the arrival order that falls out of that — left to right — becomes the next round's
input. Repeat until sorted, or until the same arrangement comes back and the group
is stuck in a loop.

Utility function
----------------
For a candidate stall s in a row of n stalls, given occupied stalls J:

    U(s) = 1/(s+1) + 1/(n-s)  -  awkwardness * Σ(1 / |s - j|)  for j in J

    1/(s+1)       — attraction from the left wall (distance s+1 away).
    1/(n-s)       — attraction from the right wall (distance n-s away).
    Σ(1 / |s-j|) — total repulsion from ALL occupied stalls, each weighted
                   by inverse distance. A neighbour at distance 1 contributes
                   1.0; at distance 2, 0.5; at distance 4, 0.25.
                   Two neighbours at distance 1 give pressure 2.0 —
                   being squeezed hurts proportionally more.
    awkwardness   — ∈ [0, 1]. How much discomfort the person feels around
                   close neighbours. 0.0: don't care. 1.0: maximise distance
                   from everyone.

Walls and people use the same inverse-distance physics — walls attract,
people repel.

Round structure
---------------
Each round: the n values enter n stalls one-by-one in their current order.
Reading the occupied stalls left→right gives the new ordering.
Repeat until sorted or until a repeated ordering is detected (cycle).

The values themselves never affect stall selection — only n (the number of
stalls) and the positions already occupied matter. A value of 65 in a 6-element
list occupies stall 0–5, not stall 65.
"""

import itertools
import random
import time

import numpy as np
from pydantic import BaseModel, Field, ValidationError as _ValidationError

from rich import box
from rich.panel import Panel
from rich.rule import Rule
from rich.table import Table

from .utils import console, make_sort_header


# Internal policy constants.
DEFAULT_AWKWARDNESS = 0.5
STEP_DELAY = 0.12
ROUND_DELAY = 0.20

ENTRY_REMARKS_FIRST = [
    "Walks in, scans the room. Coast is clear.",
    "First one in. Takes a deep breath. Picks a spot.",
    "Empty restroom. The dream scenario.",
    "No one here. Maximum personal space achieved.",
]

ENTRY_REMARKS_COMFORTABLE = [
    "Plenty of space. No eye contact needed.",
    "Acceptable buffer zone. Proceeds with confidence.",
    "Adequate distance from neighbours. Relaxed.",
    "Low pressure. Almost comfortable.",
]

ENTRY_REMARKS_AWKWARD = [
    "This is... closer than ideal.",
    "Tries not to make eye contact.",
    "Stares straight ahead. Intensely.",
    "Whistles nervously.",
    "Regrets not waiting.",
    "The proximity is... noted.",
]

ENTRY_REMARKS_DIRE = [
    "Oh no. Oh no no no.",
    "This violates at least three unwritten rules.",
    "Maximum discomfort achieved.",
    "Considers leaving and coming back later.",
    "The awkwardness is palpable.",
]


class _UrinalSortParams(BaseModel):
    awkwardness: float = Field(ge=0.0, le=1.0)
    max_rounds: int = Field(ge=1)


def create_header():
    return make_sort_header("🚽", "urinal", "Maximise distance, then reluctantly sort", "cyan")


def _slot_utility(slots, pressure, size, awkwardness):
    """Return utility score array for all empty slots."""
    slots = np.asarray(slots, dtype=float)
    wall_affinity = 1.0 / (slots + 1) + 1.0 / (size - slots)
    return wall_affinity - awkwardness * pressure


def _choose_slot(size, occupied, awkwardness):
    """Return (slot, chosen_pressure)."""
    occupied_arr = np.asarray(occupied, dtype=int)
    empty_arr = np.setdiff1d(np.arange(size), occupied_arr)

    first_entrant = occupied_arr.size == 0
    if first_entrant:
        pressure = np.zeros(empty_arr.size)
    else:
        diff = np.abs(empty_arr[:, None] - occupied_arr[None, :]).astype(float)
        pressure = (1.0 / diff).sum(axis=1)

    utilities = _slot_utility(empty_arr, pressure, size, awkwardness)
    chosen_idx = int(np.argmax(utilities))

    return int(empty_arr[chosen_idx]), (None if first_entrant else float(pressure[chosen_idx]))


def _render_stalls(stalls, latest_slot=None):
    """Return a Rich-markup stall row string, highlighting the freshly occupied slot."""
    parts = []
    for i, v in enumerate(stalls):
        if v is None:
            parts.append("[dim] 🚽 [/dim]")
        elif i == latest_slot:
            parts.append(f"[bold cyan]🧍{v:<2}[/bold cyan]")
        else:
            parts.append(f"[white]🧍{v:<2}[/white]")
    return " ".join(parts)


def urinal_sort(
    numbers,
    max_rounds=200,
    awkwardness=DEFAULT_AWKWARDNESS,
):
    """
    Run urinal-etiquette rounds until sorted or a cycle is detected.

    Each round: values enter stalls in current order, each picking the
    highest-utility empty stall. Reading stalls left→right gives the new ordering.

    Returns (result, rounds_taken, round_logs, did_sort)
      result       — final list (sorted if did_sort, else last state)
      rounds_taken — number of complete rounds executed
      round_logs   — list of per-round dicts with entry/output data
      did_sort     — True if result is sorted, False if cycle or limit hit
    """
    _UrinalSortParams(awkwardness=awkwardness, max_rounds=max_rounds)

    n = len(numbers)
    target = sorted(numbers)
    current = list(numbers)
    round_logs = []
    seen = {}

    console.print()
    console.print(create_header())
    console.print()
    console.print(
        f"  [dim]Input:[/dim]  [bold cyan]{list(numbers)}[/bold cyan]\n"
        f"  [dim]Target:[/dim] [bold green]{target}[/bold green]\n"
        f"  [dim]Awkwardness:[/dim] [bold magenta]{awkwardness:.2f}[/bold magenta]\n"
        f"  [dim]Strategy:[/dim] pick the least exposed stall, "
        f"read left\u2192right, repeat.\n"
    )

    if current == target:
        console.print(Rule(
            "[bold green]Already sorted. No awkward shuffling required.[/bold green]",
            style="green",
        ))
        return current, 0, [], True

    for round_num in range(max_rounds):
        state_key = tuple(current)
        if state_key in seen:
            console.print(Rule(
                f"[bold red]💀 Cycle detected — same ordering last seen in "
                f"round {seen[state_key] + 1}. "
                f"These people will never sort themselves out.[/bold red]",
                style="red",
            ))
            console.print()
            return current, round_num, round_logs, False

        seen[state_key] = round_num
        stalls = [None] * n
        occupied = []
        entries = []

        console.print(Rule(f"[bold cyan]Round {round_num + 1}[/bold cyan]", style="cyan"))
        console.print(f"  [dim]Entering order:[/dim] [bold]{current}[/bold]")
        console.print()

        for value in current:
            slot, chosen_pressure = _choose_slot(n, occupied, awkwardness)
            stalls[slot] = value
            occupied.append(slot)
            entries.append(
                {
                    "value": value,
                    "slot": slot,
                    "pressure": chosen_pressure,
                }
            )

            stall_str = _render_stalls(stalls, latest_slot=slot)
            if chosen_pressure is None:
                note = "[dim]first in — no neighbours yet[/dim]"
                remark = random.choice(ENTRY_REMARKS_FIRST)
            elif chosen_pressure < 0.8:
                note = f"[green]pressure {chosen_pressure:.2f}[/green]"
                remark = random.choice(ENTRY_REMARKS_COMFORTABLE)
            elif chosen_pressure < 1.5:
                note = f"[yellow]pressure {chosen_pressure:.2f}[/yellow]"
                remark = random.choice(ENTRY_REMARKS_AWKWARD)
            else:
                note = f"[red]pressure {chosen_pressure:.2f}[/red]"
                remark = random.choice(ENTRY_REMARKS_DIRE)

            time.sleep(STEP_DELAY)
            console.print(
                f"  [bold cyan]{value:>4}[/bold cyan] → stall [bold]{slot}[/bold]"
                f"  {stall_str}  {note}"
            )
            console.print(f"         [dim italic]{remark}[/dim italic]")

        output = list(stalls)
        is_sorted_out = output == target
        round_logs.append(
            {
                "round": round_num + 1,
                "input": list(current),
                "entries": entries,
                "output": output,
                "sorted": is_sorted_out,
            }
        )

        if is_sorted_out:
            console.print()
            console.print(f"  [bold green]Reading stalls: {output}  ✓ SORTED![/bold green]")
            console.print()
            return output, round_num + 1, round_logs, True

        console.print()
        console.print(f"  [dim]Reading stalls: {output}  ✗ not sorted[/dim]")
        console.print()
        time.sleep(ROUND_DELAY)
        current = output

    console.print(Rule(
        f"[bold red]🚽 Gave up after {max_rounds} round(s). Still not sorted.[/bold red]",
        style="red",
    ))
    return current, max_rounds, round_logs, False


def create_result_table(original, result, rounds_taken, round_logs, did_sort, awkwardness):
    table = Table(
        title="� Urinal Sort",
        box=box.ROUNDED,
        title_style="bold yellow",
        show_header=True,
        header_style="bold cyan",
    )
    table.add_column("Property", style="dim")
    table.add_column("Value", style="cyan")

    all_entries = list(itertools.chain.from_iterable(rnd["entries"] for rnd in round_logs))
    entries_total = len(all_entries)
    avg_pressure = (
        sum(e["pressure"] for e in all_entries if e["pressure"] is not None) / entries_total
        if entries_total else 0.0
    )
    outcome = (
        "[bold green]Sorted ✓[/bold green]"
        if did_sort
        else "[bold red]Unsortable (cycle detected) ✗[/bold red]"
    )

    table.add_row("Original", str(original))
    table.add_row("Result", f"[bold]{result}[/bold]")
    table.add_row("Awkwardness", f"[magenta]{awkwardness:.2f}[/magenta]")
    table.add_row("Rounds taken", str(rounds_taken))
    table.add_row("Personal space violations", str(entries_total))
    table.add_row("Avg discomfort", f"[magenta]{avg_pressure:.2f}[/magenta]")
    table.add_row("Outcome", outcome)

    return table


def create_result_panel(original, result, rounds_taken, did_sort):
    if did_sort:
        return Panel(
            f"[bold green]Sorted in {rounds_taken} round(s). "
            f"The etiquette happened to produce it.[/bold green]\n\n"
            f"[dim]Original:[/dim] {original}\n"
            f"[dim]Sorted:[/dim]   [bold cyan]{result}[/bold cyan]",
            title="[bold yellow]🚽 Final Stall Report[/bold yellow]",
            box=box.DOUBLE,
            style="green",
        )

    return Panel(
        "[bold red]The occupants have settled into a loop.\n"
        "They will never sort themselves out.\n"
        "Literally.[/bold red]\n\n"
        f"[dim]Original:[/dim]   {original}\n"
        f"[dim]Last state:[/dim] [bold cyan]{result}[/bold cyan]",
        title="[bold yellow]🚽 Final Stall Report[/bold yellow]",
        box=box.DOUBLE,
        style="red",
    )
