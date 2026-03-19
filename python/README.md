# Big O(No) — Python CLI

CLI-only implementation of intentionally impractical sorting algorithms.

## Install

```bash
pip install big-oh-no
```

## Usage

```bash
big-oh-no --help

# Wait Sort — patience is a virtue
big-oh-no wait 5 2 8 1 3

# Stalin Sort — elements that aren't in order get removed
big-oh-no stalin 5 1 9 2 8 3 10

# Linus Sort — your list gets reviewed, harshly
big-oh-no linus 3 1 7 2 9 5 12

# Bogo Sort — shuffle until it works
big-oh-no bogo 3 2 1
big-oh-no bogo --max-attempts 5000 3 2 1

# Schrödinger Sort — sorted and unsorted until observed
big-oh-no schrodinger 5 3 1 4
big-oh-no schrodinger --meanness 0.8 5 3 1 4

# Urinal Sort — elements pick positions based on personal space
big-oh-no urinal 8 3 6 1 9 2
big-oh-no urinal --awkwardness 1.0 8 3 6 1 9 2

# Digit Sort — sorts by number of digits, not value
big-oh-no digit 170 45 75 90 2 802 66

# Darwin Sort — survival of the fittest permutation
big-oh-no darwin 5 3 1 4 2
big-oh-no darwin --max-generations 200 9 1 8 2 7
big-oh-no darwin --population-size 100 --mutation-rate 0.5 5 3 1 4 2

# Vibe Sort — ask an AI to sort it for you
big-oh-no vibe 5 3 1 4 2
big-oh-no vibe --pro 5 3 1 4 2
```

## Validation

Input is validated at the CLI boundary using Pydantic v2. `numbers` must be a non-empty list of integers. Invalid input exits with a clear error message — no sorting happens.

---

## Development

### Setup

```bash
cd python
uv sync
uv run big-oh-no --help
```

Quick run without installing:

```bash
uvx --from . big-oh-no --help
```

If you see a `VIRTUAL_ENV ... does not match the project environment path` warning, another virtualenv is active in your shell. It is safe to ignore, or run `deactivate` before `uv` commands.

### Tests

```bash
uv run --extra dev pytest -q
```

Three test modules:
- `tests/test_validation.py` — Pydantic input validation
- `tests/test_algorithms.py` — sort function unit tests
- `tests/test_cli.py` — E2E CLI tests via Click's `CliRunner`

### Adding a new algorithm

- Create `big_oh_no/<name>_sort.py` with a single public sort function. The first return value must always be the sorted list — after that, return whatever the algorithm's persona demands (eliminated elements, total time, hurt feelings, etc.)
- Add a command in `big_oh_no/cli.py` using Click, following the pattern of the existing commands
- Add at least one test in `tests/test_algorithms.py`
- Update the algorithm list in the root `README.md`
- Add a run example in `python/README.md`

### Making an existing one better

- Richer Rich output, more flavourful commentary, better edge-case handling — all welcome
- Do not change the return contract of the sort function without updating `big_oh_no/cli.py` and the tests

All tests must pass before opening a PR:

```bash
uv run --extra dev pytest -q
```
