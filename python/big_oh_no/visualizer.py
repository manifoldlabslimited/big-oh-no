#!/usr/bin/env python3
"""
Sorting visualizer — animated vertical bar charts with sound.

Any algorithm yields VizFrames. The visualizer renders them as a bar chart
panel with a live text log below it — all in one Rich Live display.

Sound requires ``sounddevice`` and ``numpy`` (optional: ``pip install big-oh-no[viz]``).
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Iterator

from rich import box
from rich.console import Console, Group
from rich.live import Live
from rich.panel import Panel
from rich.text import Text


class Action(str, Enum):
    COMPARE = "compare"
    SWAP = "swap"
    ELIMINATE = "eliminate"
    INSERT = "insert"
    SHUFFLE = "shuffle"
    PLACE = "place"
    EVOLVE = "evolve"
    OBSERVE = "observe"
    VIBE = "vibe"
    DONE = "done"


_STYLES = {
    Action.COMPARE: "yellow",
    Action.SWAP: "cyan",
    Action.ELIMINATE: "red",
    Action.INSERT: "green",
    Action.SHUFFLE: "magenta",
    Action.PLACE: "green",
    Action.EVOLVE: "blue",
    Action.OBSERVE: "magenta",
    Action.VIBE: "magenta",
    Action.DONE: "bright_green",
}


@dataclass
class VizFrame:
    """A single snapshot of the algorithm's state."""
    bars: list[int]
    highlighted: list[int] = field(default_factory=list)
    action: Action = Action.COMPARE
    label: str = ""
    log_line: str = ""  # Rich-markup line to append to the running log


# ── Sound ────────────────────────────────────────────────────────────────────

_HAS_AUDIO = None


def _check_audio() -> bool:
    global _HAS_AUDIO
    if _HAS_AUDIO is None:
        try:
            import numpy  # noqa: F401
            import sounddevice  # noqa: F401
            _HAS_AUDIO = True
        except ImportError:
            _HAS_AUDIO = False
    return _HAS_AUDIO


def _value_to_freq(value: int, max_val: int) -> float:
    if max_val <= 0:
        return 400.0
    return 200 + (value / max_val) * 1200


def _make_tone(frequency: float, duration_ms: int, sr: int = 44100):
    import numpy as np
    n_samples = int(sr * duration_ms / 1000)
    t = np.linspace(0, duration_ms / 1000, n_samples, False)
    env = np.ones(n_samples)
    fade = min(n_samples // 4, int(sr * 0.005))
    if fade > 0:
        env[-fade:] = np.linspace(1, 0, fade)
    return (np.sin(2 * np.pi * frequency * t) * env * 0.25).astype(np.float32)


def _play_sound(frame: VizFrame, max_val: int) -> None:
    if not frame.highlighted or not _check_audio():
        return
    vals = [frame.bars[i] for i in frame.highlighted if i < len(frame.bars)]
    if not vals:
        return
    try:
        import numpy as np
        import sounddevice as sd
        sr = 44100
        chunks: list[np.ndarray] = []

        if frame.action == Action.ELIMINATE:
            f = _value_to_freq(vals[0], max_val)
            chunks.append(_make_tone(f, 40, sr))
            chunks.append(_make_tone(f * 0.5, 40, sr))
        elif frame.action in (Action.SWAP, Action.COMPARE):
            for v in vals:
                chunks.append(_make_tone(_value_to_freq(v, max_val), 40, sr))
        elif frame.action == Action.DONE:
            for v in sorted(vals):
                chunks.append(_make_tone(_value_to_freq(v, max_val), 30, sr))
        else:
            avg = sum(vals) / len(vals)
            chunks.append(_make_tone(_value_to_freq(int(avg), max_val), 50, sr))

        if chunks:
            sd.play(np.concatenate(chunks), sr)
            sd.wait()
    except Exception:
        pass


# ── Bar chart rendering ──────────────────────────────────────────────────────

_FULL = "█"
_CHART_HEIGHT = 16


def _build_chart(frame: VizFrame, max_val: int, algo_name: str) -> Panel:
    """Build a Rich Panel with vertical bars for one frame."""
    bars = frame.bars
    n = len(bars)
    if n == 0:
        return Panel("(empty)", title=algo_name)

    highlight_set = set(frame.highlighted)
    style = _STYLES.get(frame.action, "white")

    lines: list[Text] = []
    for row in range(_CHART_HEIGHT, 0, -1):
        threshold = (row / _CHART_HEIGHT) * max_val
        line = Text()
        for i, val in enumerate(bars):
            if i > 0:
                line.append(" ")
            if val >= threshold:
                bar_style = f"bold {style}" if i in highlight_set else "dim cyan"
                line.append(_FULL * 2, style=bar_style)
            else:
                line.append("  ")
        lines.append(line)

    # Number labels.
    num_line = Text()
    for i, val in enumerate(bars):
        if i > 0:
            num_line.append(" ")
        num_style = f"bold {style}" if i in highlight_set else "dim"
        num_line.append(f"{val:>2}", style=num_style)
    lines.append(Text("─" * (n * 3 - 1), style="dim"))
    lines.append(num_line)

    status = Text(f"\n {frame.label}", style="dim italic")
    chart_text = Text("\n").join(lines)

    panel_style = style if frame.action == Action.DONE else "dim"
    return Panel(
        Group(chart_text, status),
        title=f"[bold]{algo_name}[/bold]  [{style}]{frame.action.value}[/{style}]",
        box=box.ROUNDED,
        style=panel_style,
        padding=(1, 2),
    )


def _build_display(chart_panel: Panel, log_lines: list[str], console: Console) -> Group:
    """Combine the chart panel and the growing text log into one renderable."""
    parts: list = [chart_panel]
    if log_lines:
        log_text = Text()
        for line in log_lines:
            log_text.append_text(Text.from_markup(line + "\n"))
        parts.append(log_text)
    return Group(*parts)


# ── Public API ───────────────────────────────────────────────────────────────

def run_visualization(
    frames: Iterator[VizFrame],
    algo_name: str = "Sort",
    delay: float = 0.05,
    sound: bool = True,
) -> list[int]:
    """Animate VizFrames as a vertical bar chart with a live text log below.

    The chart panel and log lines render together in one Live display.
    The generator is responsible for yielding its own DONE frame.
    Returns the final bar state.
    """
    console = Console()
    max_val = 0
    final_bars: list[int] = []
    log_lines: list[str] = []

    with Live(console=console, refresh_per_second=20, transient=False) as live:
        for frame in frames:
            if max_val == 0 and frame.bars:
                max_val = max(frame.bars)

            if frame.log_line:
                log_lines.append(frame.log_line)

            chart = _build_chart(frame, max_val or 1, algo_name)
            live.update(_build_display(chart, log_lines, console))
            final_bars = list(frame.bars)

            if sound:
                _play_sound(frame, max_val)

            # Linger on the final frame so the user can see it.
            pause = delay * 6 if frame.action == Action.DONE else delay
            time.sleep(pause)

    return final_bars


__all__ = ["Action", "VizFrame", "run_visualization"]
