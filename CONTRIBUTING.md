# Contributing

Found another impractical sorting algorithm? Want to make an existing one better, funnier, or more dramatic? PR welcome.

**Three rules. That's it.**

1. It must actually sort a list of numbers.
2. It must run in the CLI.
3. The algorithm must either be completely useless, have a strong persona, or both.

## What "sorts correctly" means here

The final output must be in non-descending order. Side effects — data loss, drama, waiting an unreasonable amount of time — are features, not bugs.

---

## What do you want to do?

### Add or support a new language

Each language lives in its own top-level folder (e.g. `python/`, `rust/`). To add one:

- Create `<language>/` at the repo root
- Implement the CLI using whatever is idiomatic for that language
- Implement whichever algorithms you like — you don't need to port everything
- Add a `<language>/README.md` with setup, run, and contribution instructions (see [python/README.md](python/README.md) as a reference)
- Update the implementation status table in the root `README.md`
- Add a run example in `python/README.md`

### Contribute to an existing language

See the README for the language you want to work on:

- [Python](python/README.md)

---

## Commits and releases

This project uses [Conventional Commits](https://www.conventionalcommits.org/). A git hook enforces the format locally — set it up once after cloning:

```bash
uv sync --extra dev
uv run pre-commit install --hook-type commit-msg
```

After that, any commit with a non-conforming message will be rejected before it leaves your machine.

Every push to `main` is automatically processed by [python-semantic-release](https://python-semantic-release.readthedocs.io/), which reads commit messages to determine the next version, create a GitHub release, and publish to PyPI — no manual tagging required.

### Commit format

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

| Type | What it triggers |
|------|-----------------|
| `feat:` | Minor version bump — new feature |
| `fix:` | Patch version bump — bug fix |
| `perf:` | Patch version bump — performance improvement |
| `feat!:` or `BREAKING CHANGE:` footer | Major version bump |
| `chore:`, `ci:`, `docs:`, `refactor:`, `style:`, `test:` | No release |

### Examples

```
feat: add bubble sort variant
fix: handle empty list in bogo sort
perf: cache sorted check in schrodinger sort
feat!: remove wait-sort (breaks CLI)
```

A `BREAKING CHANGE:` footer also triggers a major bump:

```
feat: overhaul CLI interface

BREAKING CHANGE: --algorithm flag renamed to --sort
```

If your PR contains multiple unrelated changes, use multiple commits rather than squashing — PSR reads each commit individually to determine the version bump type.
