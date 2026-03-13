# Big O(No) 🤦‍♂️

> *A collection of utterly useless yet entertaining sorting algorithms*

```
    ██████╗ ██╗ ██████╗      ██████╗ ██╗███╗   ██╗ ██████╗ ██╗
    ██╔══██╗██║██╔════╝     ██╔═══██╗╚██╗██╔╝ ██║██╔═══██╗██║
    ██████╔╝██║██║  ███╗    ██║   ██║ ╚███╔╝  ██║██║   ██║██║
    ██╔══██╗██║██║   ██║    ██║   ██║ ██╔██╗  ██║██║   ██║╚═╝
    ██████╔╝██║╚██████╔╝    ╚██████╔╝██╔╝ ██╗ ██║╚██████╔╝██╗
    ╚═════╝ ╚═╝ ╚═════╝      ╚═════╝ ╚═╝  ╚═╝ ╚═╝ ╚═════╝ ╚═╝
```

**Big O(No)** is a lovingly curated collection of sorting algorithms that should never, ever be used. Each algorithm comes with its own unique persona and distinctive approach to achieving "sorted" results.

Some lose data. Some take forever. All are completely impractical. **But they're fun.**

---

## 🎭 Available Algorithms

| Algorithm | Persona | Method | Complexity | Output |
|-----------|---------|--------|------------|--------|
| **Wait Sort** | ⏳ The Patient One | Each number waits (value × scale) seconds | O(max(n)) time | Sorted ✓ |
| **Stalin Sort** | ☭ The Authoritarian | Eliminates out-of-order elements | O(n) time, O(n) casualties | "Sorted" ✓ |
| **Linus Sort** | 🐧 The Code Reviewer | NAKs patches that break monotonic order | O(n) time, O(n) hurt feelings | "Merged" ✓ |

---

## ⏳ Wait Sort

*"Good things come to those who wait... and wait... and wait..."*

The most patient sorting algorithm ever conceived. Each number spawns a thread that sleeps for a duration proportional to its value. Smaller numbers wake up first, naturally yielding a sorted output.

**How it works:**
1. Spawn a thread for each number
2. Each thread sleeps for `number × scale` seconds
3. When a thread wakes, it adds its number to the result
4. Smaller numbers finish first → **Sorted!**

**Complexity:**
- Time: O(max(n)) — determined by your largest number
- Space: O(n) threads
- Patience: 100% required

```bash
# Sort [5, 2, 8, 1, 3] - takes ~8 seconds
big-oh-no wait 5 2 8 1 3

# Speed it up with a scale factor
big-oh-no wait 5 2 8 1 3 --scale 0.5
```

---

## ☭ Stalin Sort

*"In Soviet Russia, list sorts YOU"*

A sorting algorithm that achieves order through elimination. Any element that dares to be smaller than the previous maximum is simply... removed. The survivors form a perfectly sorted list.

**How it works:**
1. Start with the first element as the current maximum
2. Iterate through the list
3. If element >= current max → **survives** (update max)
4. If element < current max → **eliminated** 💀
5. Survivors are sorted!

**Complexity:**
- Time: O(n)
- Space: O(1)
- Casualties: O(n)

```bash
# Input: [5, 1, 9, 2, 8, 3, 10]
# Output: [5, 9, 10]
# Eliminated: [1, 2, 8, 3]
big-oh-no stalin 5 1 9 2 8 3 10
```

---

## 🐧 Linus Sort

*"Your code is bad and you should feel bad"*

Each element is submitted as a "patch" for review by a simulated Linus Torvalds. Patches that maintain monotonic order are merged with begrudging approval. Those that don't are NAK'd with colorful commentary.

**How it works:**
1. Submit your "patches" (numbers) for review
2. Linus reviews each one with brutal honesty
3. Patches >= current max are **merged** (barely acceptable)
4. Patches < current max are **NAK'd** (with extreme prejudice)
5. Result: A "clean" git history

**Complexity:**
- Time: O(n)
- Space: O(1)
- Hurt feelings: O(n)

```bash
# Input: [3, 1, 7, 2, 9, 5, 12]
# Merged: [3, 7, 9, 12]
# NAK'd: [1, 2, 5]
big-oh-no linus 3 1 7 2 9 5 12
```

---

## 📦 Installation

### Python

```bash
cd python
uv sync

# Run directly
uv run big-oh-no

# Or with specific algorithm
uv run big-oh-no stalin 5 1 9 2 8
```

### Rust

🦀 *Coming soon...*

---

## 🚀 Usage

```bash
# Show available algorithms
big-oh-no

# Run a specific algorithm
big-oh-no <algorithm> [numbers...]

# Get help
big-oh-no --help
big-oh-no <algorithm> --help
```

### Examples

```bash
# Wait Sort with custom scale
big-oh-no wait 10 5 3 7 --scale 0.5

# Stalin Sort
big-oh-no stalin 5 1 9 2 8 3 10

# Linus Sort
big-oh-no linus 3 1 7 2 9 5 12
```

### Validation

- Input validation uses Pydantic v2 at the CLI boundary.
- `numbers` must be a non-empty list of integers.
- For Wait Sort, `scale` must be a positive number.

---

## 🧪 Testing

```bash
cd python
uv run --extra dev pytest -q
```

---

## 🗂️ Project Structure

```
big-oh-no/
├── README.md           # You are here
├── python/             # Python implementation
│   ├── pyproject.toml  # Project config
│   ├── cli.py          # Click CLI
│   ├── wait_sort.py    # Wait Sort implementation
│   ├── stalin_sort.py  # Stalin Sort implementation
│   └── linus_sort.py   # Linus Sort implementation
└── rust/               # Rust implementation (coming soon)
    └── src/
```

---

## 📊 Implementation Status

| Algorithm | Python | Rust |
|-----------|:------:|:----:|
| Wait Sort | ✅ | 🚧 |
| Stalin Sort | ✅ | 🚧 |
| Linus Sort | ✅ | 🚧 |

---

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

---

## 📜 License

MIT — Use these algorithms in production at your own risk. (Please don't.)

---

## 🙏 Acknowledgments

- **Wait Sort** — Inspired by the concept of Sleep Sort
- **Stalin Sort** — Inspired by the infamous "Stalin Sort" meme
- **Linus Sort** — Inspired by Linus Torvalds' legendary code review style on LKML

---

<p align="center">
  <i>Remember: Just because you can sort this way doesn't mean you should.</i>
</p>

<p align="center">
  <b>Big O(No)</b> — Where algorithms go to die... entertainingly.
</p>
