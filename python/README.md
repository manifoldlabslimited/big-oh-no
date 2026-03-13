# Big O(No) — Python CLI

CLI-only implementation of intentionally impractical sorting algorithms.

## Run

```bash
cd python
uv sync
uv run big-oh-no --help
uv run big-oh-no wait 5 2 8 1 3
uv run big-oh-no stalin 5 1 9 2 8 3 10
uv run big-oh-no linus 3 1 7 2 9 5 12
```

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

- Create `<name>_sort.py` with a single public sort function. The first return value must always be the sorted list — after that, return whatever the algorithm's persona demands (eliminated elements, total time, hurt feelings, etc.)
- Add a command in `cli.py` using Click, following the pattern of the existing commands
- Add at least one test in `tests/test_algorithms.py`
- Update the algorithm list in the root `README.md`

### Making an existing one better

- Richer Rich output, more flavourful commentary, better edge-case handling — all welcome
- Do not change the return contract of the sort function without updating `cli.py` and the tests

All tests must pass before opening a PR:

```bash
uv run --extra dev pytest -q
```
