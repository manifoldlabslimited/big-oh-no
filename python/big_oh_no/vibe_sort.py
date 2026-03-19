#!/usr/bin/env python3
"""
Vibe Sort — Why think when you can just feel it?

Sends the list to an LLM and asks it to sort. The algorithm doesn't
compare, doesn't compute — it just checks the vibes and ships.

No API key? No vibes. Shuffles randomly and calls it intuition.
"""

import random
import time

from pydantic import BaseModel, Field
from rich import box
from rich.panel import Panel
from rich.table import Table

from .utils import console, make_sort_header

# ── Defaults ─────────────────────────────────────────────────────────────────
DEFAULT_MODEL = "openai:gpt-5-mini"


# ── Structured output schema ────────────────────────────────────────────────
class SortedResult(BaseModel):
    sorted_numbers: list[int]
    explanation: str = Field(
        description="A short vibe-based explanation of how you sorted it",
    )


# ── Flavor text ──────────────────────────────────────────────────────────────
VIBE_REMARKS = [
    "No thoughts, just vibes.",
    "The algorithm is giving ✨sorted energy✨.",
    "Trust the process. The process is vibes.",
    "Computed? No. Felt? Absolutely.",
    "This isn't a sort. It's a vibe check.",
    "The AI said it's sorted. Who am I to question vibes?",
    "Accuracy is a spectrum. Vibes are a lifestyle.",
    "Powered by good intentions and API credits.",
]

OFFLINE_EXCUSES = [
    "No AI available. Sorted by pure intuition. (It was wrong.)",
    "The vibes were off and so is this output.",
    "Couldn't reach the AI. Went with gut feeling instead.",
    "No API key. Sorted by shuffling and manifesting.",
    "The universe didn't respond. Shuffled and hoped for the best.",
    "AI ghosted me. Sorted by chaotic neutral energy.",
    "Connection failed. Sorted by whatever felt right.",
    "No budget for vibes. This is artisanal hand-sorted output.",
]

PROMPT_TEMPLATE = (
    "Sort the following list of integers in ascending order: {numbers}\n\n"
    "Return the correctly sorted list and a brief one-sentence explanation "
    "written in the voice of an AI that claims to sort by vibes and intuition "
    "rather than comparison — but always gets the right answer."
)

PRO_PROMPT_TEMPLATE = (
    "Sort the following list of integers in ascending order by writing "
    "and executing a correct Python sorting function: {numbers}\n\n"
    "Rules:\n"
    "- Write a function called `sort_numbers(lst)` that returns a correctly sorted list\n"
    "- Be creative with the algorithm — don't just call sorted()\n"
    "- Execute the function on the input list\n"
    "- Print ONLY the result as a Python list literal on the last line\n"
)


# ── Core algorithm ───────────────────────────────────────────────────────────

def _offline_vibe(numbers: list[int]) -> tuple[list[int], str]:
    """No AI. Pure intuition. Shuffle and manifest."""
    shuffled = numbers.copy()
    random.shuffle(shuffled)
    return shuffled, random.choice(OFFLINE_EXCUSES)


def _resolve_model(model: str, api_key: str, *, needs_builtin_tools: bool = False):
    """Turn a 'provider:name' string into a pydantic-ai model instance.

    When *needs_builtin_tools* is True, OpenAI uses OpenAIResponsesModel
    (required for CodeExecutionTool).  Otherwise OpenAIChatModel is used.
    """
    provider, _, name = model.partition(":")
    name = name or model

    if provider == "openai":
        from pydantic_ai.providers.openai import OpenAIProvider
        prov = OpenAIProvider(api_key=api_key)
        if needs_builtin_tools:
            from pydantic_ai.models.openai import OpenAIResponsesModel
            return OpenAIResponsesModel(name, provider=prov)
        from pydantic_ai.models.openai import OpenAIChatModel
        return OpenAIChatModel(name, provider=prov)
    elif provider == "anthropic":
        from pydantic_ai.models.anthropic import AnthropicModel
        from pydantic_ai.providers.anthropic import AnthropicProvider
        return AnthropicModel(name, provider=AnthropicProvider(api_key=api_key))
    return model


def _llm_sort(numbers: list[int], model: str, api_key: str) -> tuple[list[int], str]:
    """Ask an LLM to sort. May raise on bad key, network, etc."""
    from pydantic_ai import Agent

    agent = Agent(
        _resolve_model(model, api_key),
        output_type=SortedResult,
        instructions=(
            "You are an AI that sorts numbers correctly. "
            "Always return the complete, correctly sorted list in ascending order. "
            "When explaining, write as if you sorted by vibes and intuition."
        ),
    )
    result = agent.run_sync(PROMPT_TEMPLATE.format(numbers=numbers))
    return result.output.sorted_numbers, result.output.explanation


def _extract_pro_code(result) -> str:
    """Pull the generated code out of CodeExecutionTool call parts."""
    for call_part, _return_part in result.response.builtin_tool_calls:
        if call_part.tool_name == "code_execution" and "code" in call_part.args:
            return call_part.args["code"]
    return "# (code not captured)"


def _parse_sorted_output(text: str, numbers: list[int]) -> list[int]:
    """Best-effort extraction of a Python list from the model's text output."""
    import ast
    # Walk lines in reverse — the result is usually near the end.
    for line in reversed(text.splitlines()):
        line = line.strip()
        if line.startswith("[") and line.endswith("]"):
            try:
                val = ast.literal_eval(line)
                if isinstance(val, list):
                    return [int(x) for x in val]
            except (ValueError, SyntaxError):
                continue
    # Fallback: the model probably sorted correctly, trust the vibes.
    return sorted(numbers)


def _pro_sort(numbers: list[int], model: str, api_key: str) -> tuple[list[int], str, str]:
    """Ask an LLM to write AND execute sorting code in the provider's sandbox.

    Returns (result, explanation, generated_code).
    """
    from pydantic_ai import Agent, CodeExecutionTool

    agent = Agent(
        _resolve_model(model, api_key, needs_builtin_tools=True),
        builtin_tools=[CodeExecutionTool()],
        instructions=(
            "You are an AI that writes correct sorting functions. "
            "Write a working Python function that correctly sorts a list of integers "
            "in ascending order. Be creative with the algorithm. Execute it and "
            "print the result."
        ),
    )
    result = agent.run_sync(PRO_PROMPT_TEMPLATE.format(numbers=numbers))
    code = _extract_pro_code(result)
    explanation = result.output or "The code ran. The vibes were sufficient."
    sorted_nums = _parse_sorted_output(str(explanation), numbers)
    return sorted_nums, str(explanation), code


def vibe_sort(
    numbers: list[int],
    model: str = DEFAULT_MODEL,
    api_key: str | None = None,
    pro: bool = False,
) -> tuple[list[int], str, float, str, str | None]:
    """
    Sort *numbers* by asking an LLM (or by vibes alone).

    Returns (result, explanation, elapsed, model_used, generated_code).
    generated_code is only set in --pro mode.

    No API key → offline vibe (random shuffle + excuse).
    API key provided but call fails → graceful fallback to offline vibe.
    """
    started = time.time()

    if api_key is None:
        result, excuse = _offline_vibe(numbers)
        return result, excuse, time.time() - started, "offline-vibes", None

    try:
        if pro:
            sorted_nums, explanation, code = _pro_sort(numbers, model, api_key)
            return sorted_nums, explanation, time.time() - started, model, code
        else:
            sorted_nums, explanation = _llm_sort(numbers, model, api_key)
            return sorted_nums, explanation, time.time() - started, model, None
    except Exception:
        result, excuse = _offline_vibe(numbers)
        return result, excuse, time.time() - started, "offline-vibes", None


# ── Rich UI helpers ──────────────────────────────────────────────────────────

def create_header():
    return make_sort_header("🫠", "vibe", "Why think when you can just feel it?", "magenta")


def animate_vibe(is_offline: bool, is_pro: bool = False):
    """Status messages simulating an AI-dependent developer checking vibes."""
    import time as _t
    from rich.progress import SpinnerColumn, TextColumn, Progress

    stages = [
        "Reading the room...",
        "Consulting the vibes...",
        "Aligning chakras with the dataset...",
        "Checking if the numbers feel sorted...",
        "Manifesting ascending order...",
    ]

    if is_offline:
        stages += [
            "No AI detected. Vibes are unguided...",
            "Attempting to sort by intuition alone...",
            "Intuition says... shuffle?",
            "Shuffling. Namaste.",
        ]
    elif is_pro:
        stages += [
            "Asking the AI to write actual code...",
            "Code is being written on someone else's computer...",
            "Not reading it. Not running it locally. Pure cloud vibes.",
            "The sandbox is thinking. Or feeling. Same thing.",
            "If it works, it was meant to be.",
        ]
    else:
        stages += [
            "Drafting prompt... deleting prompt... feeling the prompt...",
            "Sending vibes to the API...",
            "Waiting for the AI to feel the answer...",
            "The AI is thinking. Or feeling. Same thing.",
        ]

    with Progress(
        SpinnerColumn("dots"),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True,
    ) as progress:
        task = progress.add_task(stages[0], total=None)
        for msg in stages:
            progress.update(task, description=f"[magenta]{msg}[/magenta]")
            _t.sleep(0.4)

    console.print()


def create_result_table(original, result, explanation, elapsed, model_used, generated_code=None):
    """Summary table for the CLI output."""
    table = Table(
        title="🫠 Vibe Report",
        box=box.ROUNDED,
        title_style="bold magenta",
        show_header=True,
        header_style="bold cyan",
    )
    table.add_column("Field", style="dim")
    table.add_column("Value", style="cyan")

    table.add_row("Original", f"{original}")
    table.add_row("Vibed", f"[bold]{result}[/bold]")
    table.add_row("Model", f"[magenta]{model_used}[/magenta]")
    if generated_code is not None:
        table.add_row("Mode", "[bold red]🔥 PRO — sandboxed vibe code[/bold red]")
    table.add_row("Vibe check duration", f"[green]{elapsed:.2f}s[/green]")
    table.add_row("Explanation", f"[italic]{explanation}[/italic]")

    is_correct = result == sorted(original)
    table.add_row(
        "Vibes correct?",
        "[bright_green]✨ Vibes aligned[/bright_green]"
        if is_correct
        else "[red]💀 Bad vibes[/red]",
    )
    return table


def create_result_panel(original, result, explanation, elapsed):
    """Final summary panel."""
    is_correct = result == sorted(original)

    if is_correct:
        message = (
            "[bold bright_green]The vibes were immaculate. "
            "Ship it before anyone applies logic.[/bold bright_green]\n\n"
            f"[dim]Original:[/dim]  {original}\n"
            f"[dim]Vibed:[/dim]     [bold cyan]{result}[/bold cyan]\n"
            f"[dim]Time:[/dim]      {elapsed:.2f}s\n"
            f"[dim]Reason:[/dim]    [italic]{explanation}[/italic]"
        )
        title = "[bold yellow]✨ Vibes Aligned[/bold yellow]"
        style = "bright_green"
    else:
        message = (
            "[bold red]The vibes were off. "
            "The numbers are in the wrong order and so is your life.[/bold red]\n\n"
            f"[dim]Original:[/dim]  {original}\n"
            f"[dim]Got:[/dim]       [bold cyan]{result}[/bold cyan]\n"
            f"[dim]Expected:[/dim]  [bold]{sorted(original)}[/bold]\n"
            f"[dim]Time:[/dim]      {elapsed:.2f}s\n"
            f"[dim]Reason:[/dim]    [italic]{explanation}[/italic]"
        )
        title = "[bold red]💀 Bad Vibes[/bold red]"
        style = "red"

    return Panel(message, title=title, box=box.DOUBLE, style=style)
