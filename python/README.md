# Big O(No) — Python CLI

CLI-only implementation of intentionally impractical sorting algorithms.

## Install

```bash
pip install big-oh-no
big-oh-no --help
```

## Run

Quick run (no manual environment activation):

```bash
cd python
uvx --from . big-oh-no --help
uvx --from . big-oh-no wait 5 2 8 1 3
```

Development run:

```bash
cd python
uv sync
uv run big-oh-no --help
uv run big-oh-no wait 5 2 8 1 3
uv run big-oh-no stalin 5 1 9 2 8 3 10
uv run big-oh-no linus 3 1 7 2 9 5 12
uv run big-oh-no bogo 3 2 1
uv run big-oh-no bogo --max-attempts 5000 3 2 1
uv run big-oh-no schrodinger 5 3 1 4
uv run big-oh-no schrodinger --meanness 0.8 5 3 1 4
uv run big-oh-no urinal 8 3 6 1 9 2
uv run big-oh-no urinal --awkwardness 1.0 8 3 6 1 9 2
uv run big-oh-no digit 170 45 75 90 2 802 66
uv run big-oh-no digit 3 1 4 1 5 9 2 6
```

If you see a `VIRTUAL_ENV ... does not match the project environment path` warning, another virtualenv is active in your shell. It is safe to ignore, or run `deactivate` before `uv` commands.

## Validation

Input is validated at the CLI boundary using Pydantic v2. `numbers` must be a non-empty list of integers. Invalid input exits with a clear error message — no sorting happens.

## Tests

```bash
cd python
uv run --extra dev pytest -q
```

Three test modules:
- `tests/test_validation.py` — Pydantic input validation
- `tests/test_algorithms.py` — sort function unit tests
- `tests/test_cli.py` — E2E CLI tests via Click's `CliRunner`

---

## Contributing

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
