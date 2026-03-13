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
