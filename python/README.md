## Big O(No) - Python CLI

CLI-only implementation of intentionally impractical sorting algorithms.

### Run

```bash
uv sync
uv run big-oh-no --help
uv run big-oh-no wait 5 2 8 1 3 --scale 0.5
uv run big-oh-no stalin 5 1 9 2 8 3 10
uv run big-oh-no linus 3 1 7 2 9 5 12
```

### Validation

- Pydantic v2 validates input at the CLI boundary.
- `numbers` must be a non-empty list of integers.
- `wait --scale` must be greater than `0`.

### Tests

```bash
uv run --extra dev pytest -q
```
