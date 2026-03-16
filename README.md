# Big O(No) 🤦‍♂️

> *A collection of utterly useless yet entertaining sorting algorithms*

[![CI](https://github.com/manifoldlabslimited/big-oh-no/actions/workflows/ci.yml/badge.svg)](https://github.com/manifoldlabslimited/big-oh-no/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/manifoldlabslimited/big-oh-no/graph/badge.svg?token=ad001c77-b9d4-4990-a7c8-00d96e5d7180)](https://codecov.io/gh/manifoldlabslimited/big-oh-no)
[![PyPI](https://img.shields.io/pypi/v/big-oh-no)](https://pypi.org/project/big-oh-no/)
```
┌───────────────────────────────────────────────────────────────────┐
│██████╗ ██╗ ██████╗      ██████╗ ██╗  ██╗    ███╗   ██╗ ██████╗ ██╗│
│██╔══██╗██║██╔════╝     ██╔═══██╗██║  ██║    ████╗  ██║██╔═══██╗██║│
│██████╔╝██║██║  ███╗    ██║   ██║███████║    ██╔██╗ ██║██║   ██║██║│
│██╔══██╗██║██║   ██║    ██║   ██║██╔══██║    ██║╚██╗██║██║   ██║╚═╝│
│██████╔╝██║╚██████╔╝    ╚██████╔╝██║  ██║    ██║ ╚████║╚██████╔╝██╗│
│╚═════╝ ╚═╝ ╚═════╝      ╚═════╝ ╚═╝  ╚═╝    ╚═╝  ╚═══╝ ╚═════╝ ╚═╝│
└───────────────────────────────────────────────────────────────────┘
```

**Big O(No)** is a lovingly curated collection of sorting algorithms that should never, ever be used. Each algorithm comes with its own unique persona and distinctive approach to achieving "sorted" results.

Some lose data. Some take forever. All are completely impractical. **But they're fun.**

---

## 📦 Install

```bash
pip install big-oh-no
```

## ▶️ Run

```bash
big-oh-no stalin 5 1 9 2 8 3 10   # eliminates out-of-order elements
big-oh-no linus 3 1 7 2 9 5 12    # NAKs patches that break order
big-oh-no wait 5 2 8 1 3          # takes ~8 seconds
big-oh-no bogo 3 2 1              # shuffles until sorted
big-oh-no schrodinger 5 3 1 4     # collapses to the worst outcome
big-oh-no urinal 8 3 6 1 9 2      # personal space first
big-oh-no digit 170 45 75 90 2 802 66  # bucket bureaucracy, zero comparisons
big-oh-no darwin 5 3 1 4 2            # survival of the fittest permutation
```

---

## 🎭 Algorithms

| Algorithm | Persona | Method | Complexity |
|-----------|---------|--------|------------|
| **Wait Sort** | ⏳ The Patient One | Each number waits (value) seconds in a thread | O(max(n)) time |
| **Stalin Sort** | ☭ The Authoritarian | Eliminates any element smaller than the current max | O(n) time, O(n) casualties |
| **Linus Sort** | 🐧 The Code Reviewer | NAKs patches that break monotonic order | O(n) time, O(n) hurt feelings |
| **Bogo Sort** | 🎲 The Gambler | Randomly shuffles until sorted | O((n+1)!) expected time |
| **Schrödinger Sort** | 🐱 The Quantum Observer | Collapses to least convenient state on observation | O(n log n) · O(∞) regret |
| **Urinal Sort** | 🚽 The Personal Space Enthusiast | Each person picks the stall furthest from others and closest to a wall; read left→right, repeat until sorted or a cycle is detected | O(rounds × n³) time, O(n) space |
| **Digit Sort** | 🗂️ The Bucket Bureaucrat | Routes each number to its digit bucket, pass by pass. No comparisons. Just paperwork. | O(d × n) time, 0 comparisons |
| **Darwin Sort** | 🧬 The Naturalist | Evolves a population of permutations through selection, crossover, and mutation until the sorted order emerges — or the species goes extinct | O(generations × population × n) time |

---

## ⏳ Wait Sort

*"Good things come to those who wait... and wait... and wait..."*

### Inspiration

If you put every number in a separate thread and tell each one to sleep for however many seconds its value is, the small numbers wake up first. That's it. That's the sort. No comparisons, no swaps — just time doing the work. The idea came from watching how things naturally fall into order when you let their size dictate how long they take.

The most patient sorting algorithm ever conceived. Each number spawns a thread that sleeps for a duration proportional to its value. Smaller numbers wake up first, naturally yielding a sorted output.

**How it works:**
1. Spawn a thread for each number
2. Each thread sleeps for `value` seconds
3. When a thread wakes, it adds its number to the result
4. Smaller numbers finish first → **Sorted!**

**Complexity:**
- Time: O(max(n)) — determined by your largest number
- Space: O(n) threads
- Patience: 100% required

```bash
# Sort [5, 2, 8, 1, 3] - takes ~8 seconds
big-oh-no wait 5 2 8 1 3
```

---

## ☭ Stalin Sort

*"In Soviet Russia, list sorts YOU"*

### Inspiration

Stalin ran the Soviet Union by removing people who didn't fit. Not relocating them, not giving them another chance — just gone. The scary part is it worked, in a narrow sense: the people left were the ones who conformed. The state looked organised. It just had a lot fewer people in it than it started with.

Stalin Sort does the same thing. Anything that breaks the sorted order gets deleted on the spot. What's left is sorted. Whether you still have all your numbers is not the algorithm's concern.

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

### Inspiration

Linus Torvalds built Linux and has been reviewing kernel patches for decades. He is not known for being gentle about bad code. His emails on the Linux kernel mailing list became famous — "this is garbage", "what were you thinking", flat NAKs with no explanation. The idea is that if you submit something that makes the codebase worse, it gets rejected and you feel bad about it. It keeps the tree clean.

Linus Sort applies that to numbers. Each one gets submitted as a patch. If it keeps the sequence moving forward, it's in. If it doesn't, it's NAK'd.

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

## 🎲 Bogo Sort

*"If we shuffle enough times, eventually statistics will apologize."*

### Inspiration

The infinite monkey theorem says that if you had a monkey randomly hitting keys forever, it would eventually type out any text you want — including a sorted list. This is mathematically true and completely pointless in practice. The time it would take is so absurdly long it makes the age of the universe look like nothing. Bogo Sort is the algorithm that heard this and thought "yeah, let's do that".

This algorithm keeps randomly shuffling the list and checking whether it is sorted. It is technically valid and practically awful.

**How it works:**
1. Check if the current list is sorted
2. If not, shuffle randomly
3. Repeat until sorted (or you run out of patience)

**Complexity:**
- Expected Time: O((n+1)!)
- Space: O(1)
- Reliability: Depends on luck

Optional parameter:
- `--max-attempts <n>` limits shuffle attempts before timing out (default: `10000`)

```bash
# Input: [3, 2, 1]
# Output (eventually): [1, 2, 3]
big-oh-no bogo 3 2 1

# Cap attempts for faster feedback while demoing
big-oh-no bogo --max-attempts 5000 3 2 1
```

---

## 🐱 Schrödinger Sort

*"You shouldn't have looked."*

### Inspiration

In 1935, Schrödinger came up with a thought experiment to show how weird quantum mechanics was. A cat is put in a box with a radioactive atom. If the atom decays, the cat dies. Quantum mechanics says the atom is in both states at once until observed — so the cat is simultaneously alive and dead. Schrödinger's point was that this is ridiculous and something must be wrong with the theory. Physicists mostly just kept using the maths and agreed to argue about what it means later.

Schrödinger Sort puts a list in that box. It's sorted and unsorted at the same time — both states exist in superposition until the algorithm is asked for a result. At that point the wavefunction collapses into one outcome. The bias is built in: the worse outcome is always more likely, and the `--meanness` dial controls just how spiteful the universe feels today. If the list was already sorted going in, collapse to unsorted is guaranteed — the algorithm sees a sorted input, decides that's too convenient, and deliberately destroys it. There is no kindness here. The universe observed your smugly pre-sorted list and chose violence.

All numbers survive — none are dropped. They just end up in an order that was specifically chosen to annoy.

**How it works:**
1. Take the input list and produce two versions: sorted and shuffled. Both are shown — the list is simultaneously sorted and unsorted.
2. Observe it. The act of observation collapses it into one state.
3. It collapses into whichever state is least convenient, biased by `--meanness`.
4. If the input was already sorted, it always collapses to shuffled.

**Complexity:**
- Collapse: O(1)
- Computing sorted state: O(n log n)
- Regret: O(∞)

Optional parameter:
- `--meanness <0.0–1.0>` — how spiteful the universe feels today
  - `0.0`: kind universe — you're more likely to get sorted
  - `0.5`: roughly coin-flip behaviour
  - `1.0`: spiteful universe — you're more likely to get shuffled

```bash
# Sorted or shuffled — the universe decides
big-oh-no schrodinger 5 3 1 4

# Increase the meanness for worse odds
big-oh-no schrodinger --meanness 0.8 5 3 1 4

# Already sorted — collapse to unsorted is guaranteed
big-oh-no schrodinger 1 2 3
```

---

## 🚽 Urinal Sort

*"Personal space first. Correctness by accident."*

### Inspiration

Picture a men's bathroom with a row of urinals. A group of guys walks in one by one, each wearing a jersey with a number on it. They have one goal: pick the most comfortable stall. Not to sort themselves. Not to cooperate. Just to avoid standing near anyone else. The number on the jersey is irrelevant — nobody picks a stall based on what jersey they're wearing.

There are unwritten rules everyone follows without thinking: take the stall furthest from whoever's already there. Corners beat the middle when everything else is equal. Never stand next to someone if there's a gap.

If you watch the order people end up standing in and read their jersey numbers left to right, you get a new sequence. Send them out, queue them back up in that new order, and repeat. Sometimes, after enough rounds, the jerseys are in order. Not because anyone was trying to sort. Just because the etiquette happened to produce it.

That's Urinal Sort.

### Modelling the etiquette

Each person sizes up every empty stall and picks the best one — furthest from others, closest to a wall, least exposed. That intuition collapses into a single utility score:

$$U(s) = \underbrace{\frac{1}{s+1} + \frac{1}{n-s}}_{\text{wall attraction}} - \underbrace{\alpha \sum_{j \in J} \frac{1}{|s-j|}}_{\text{neighbour repulsion}}$$

**Wall attraction** — the left wall is one step beyond stall 0 (distance $s+1$); the right wall is one step beyond stall $n-1$ (distance $n-s$). Inverse distance: the nearer you are to a wall, the more it pulls. This is why the first person always heads for a corner — no neighbours yet, so wall pull is all that matters.

**Neighbour repulsion** — for every occupied stall `j`, we add $1/d$ where $d = |s-j|$. A neighbour at distance 1 contributes 1.0; at distance 2, just 0.5. Two neighbours at distance 1 give total pressure 2.0 — being flanked hurts twice as much as one neighbour at the same distance.

Walls and people use the same physics. Walls attract, people repel.

**`awkwardness`** $\alpha \in [0, 1]$ — how much discomfort a person feels around close neighbours. At `0.0`, they don't care how close others are. At `1.0`, they want to be as far from everyone as possible.

### How it works

1. Create `n` empty stalls. The numbers queue up in their current order.
2. Each person scores every empty stall by position alone — their value is just a label, it plays no part in stall selection — and takes the highest-scoring one.
3. Once everyone's seated, read the stalls left→right — that's the new order.
4. Repeat with the new order. Stop when sorted, or when the same arrangement comes back (cycle).

### Worked example: `[1, 3, 2]` — three stalls, `awkwardness = 0.5`

```
Stalls:  0    1    2
```

**Round 1**

`1` enters first — no neighbours. Both corner stalls score $1/1 + 1/3 \approx 1.33$, the middle scores $1/2 + 1/2 = 1.0$. Corners tie; stall 0 is chosen (lower index).

```
│ 1 │   │   │
```

`3` enters (occupied: {0}):

| Stall | Wall | Repulsion | U(s) |
|---|---:|---:|---:|
| 1 | 1.00 | 1/1 = 1.00 | +0.50 |
| 2 | 1.33 | 1/2 = 0.50 | +1.08 |

Stall 2 is chosen.

```
│ 1 │   │ 3 │
```

`2` enters (occupied: {0, 2}) — only stall 1 is empty.

```
│ 1 │ 2 │ 3 │
```

Reading left→right: `[1, 2, 3]` ✓ sorted in one round.

### Counter-example: `[3, 2, 1]` — cycles immediately

`3` enters first every round — no neighbours. Both corners tie at 1.33; lower index wins. `3` takes stall 0 every round without exception.

With stall 0 taken, the second person always sees:

| Stall | Wall | Repulsion | U(s) |
|---|---:|---:|---:|
| 1 | 1.00 | 1/1 = 1.00 | +0.50 |
| 2 | 1.33 | 1/2 = 0.50 | +1.08 |

Stall 2 wins. The third person is forced into stall 1.

Reading left→right gives `[3, ?, ?]` where the second and third seats swap every round:

```
Round 1:  [3, 2, 1]  →  3→stall 0,  2→stall 2,  1→stall 1  →  reading: [3, 1, 2]
Round 2:  [3, 1, 2]  →  3→stall 0,  1→stall 2,  2→stall 1  →  reading: [3, 2, 1]
💀 Cycle detected — same ordering last seen in round 1.
```

`3` is anchored to the left corner. `1` and `2` chase each other around it forever.

**Complexity:**
- Time: O(rounds × n³)
- Space: O(n)
- Personal space violations: O(rounds × n)

**How does the number of urinals affect the chance of sorting?**

More urinals, worse odds. A lot worse. At 2 urinals it's a coin flip. At 5 the rate is down to 3%. At 8, across 200 random starting orderings, it never sorted once.

Each cell is the percentage of random starting orderings that produced a sorted result, tested at different `--max-rounds` limits:

| Urinals | max=1 | max=2 | max=3 | max=5 | max=10 | max=50 |
|---------|-------|-------|-------|-------|--------|--------|
| 2 | 50% | 50% | 50% | 50% | 50% | 50% |
| 3 | 34% | 34% | 34% | 34% | 34% | 34% |
| 4 | 9% | 13.5% | 13.5% | 13.5% | 13.5% | 13.5% |
| 5 | 2% | 3% | 3% | 3% | 3% | 3% |
| 6 | 0.5% | 0.5% | 0.5% | 0.5% | 0.5% | 0.5% |
| 8+ | 0% | 0% | 0% | 0% | 0% | 0% |

Giving it more rounds doesn't help. At 4 urinals there's a small jump from round 1 to round 2, then nothing — by round 3 everything that was going to sort already has. The reason is cycle detection: once people fall into a repeated pattern, no further rounds will break it. Either they sort early or they loop forever.

`--awkwardness` doesn't move the needle either. It was tested across every combination and the sort rates didn't budge.

Options:
- `--awkwardness <0.0–1.0>` — neighbour discomfort (0 = indifferent, 1 = maximise distance from everyone; default `0.5`)
- `--max-rounds <n>` — give up after this many rounds (default `200`; cycle detection usually fires first)

```bash
# Sorts in one round
big-oh-no urinal 1 3 2

# Cycles forever (detected immediately)
big-oh-no urinal 3 2 1

# Larger input — may sort, may cycle
big-oh-no urinal 8 3 6 1 9 2

# α=0: neighbour repulsion disabled, stall choice by wall proximity only
big-oh-no urinal --awkwardness 0.0 8 3 6 1 9 2

# α=1: neighbour repulsion at full weight
big-oh-no urinal --awkwardness 1.0 8 3 6 1 9 2
```

---

## 🗂️ Digit Sort

*"I don't rank people. I file them."*

### Inspiration

Before computers could sort data, Herman Hollerith's 1887 tabulating machines processed US census punch cards by sorting them into physical bins — one column at a time. No card was ever compared to another. Each card was simply read at the relevant column and dropped into the corresponding bin. When all bins were collected in order, the data was sorted. It was mechanical, methodical, and deeply bureaucratic.

Digit Sort is that same idea wearing a suit. Every number gets examined one digit at a time, routed to its designated bucket, and collected with all the others when the pass is complete. Nobody asks whether 802 is bigger than 45. That's not how filing works. The routing code is all that matters.

### The persona

The Bucket Bureaucrat runs the Department of Numerical Classification. Their desk is immaculate. Their procedures are documented on Form 7G. They process each number in the order received, examine the relevant digit column, and deposit the number into the appropriate bucket — no more, no less. Comparisons are not within their remit. Comparisons, in fact, are strictly prohibited under Section 4(b).

They will sort your list. They will produce the correct result. They will never once look at two numbers and decide which is bigger. And frankly, they find the idea offensive.

### How it works

1. Find the maximum number in the batch — determine how many digit columns need processing
2. Starting from the **ones digit**, route each number into bucket 0–9 based solely on that digit
3. Collect buckets 0 through 9 in order, preserving arrival order within each bucket
4. Repeat for the **tens**, **hundreds**, **thousands**, … digit columns
5. After all columns are processed, the list is sorted

**No number is ever compared to any other number.**

### Worked example

```
Input: [170, 45, 75, 90, 2, 802, 66]

Pass 1 — ones digit:
  Bucket 0: [170, 90]    (ones digit is 0)
  Bucket 2: [2, 802]     (ones digit is 2)
  Bucket 5: [45, 75]     (ones digit is 5)
  Bucket 6: [66]         (ones digit is 6)
  → [170, 90, 2, 802, 45, 75, 66]

Pass 2 — tens digit:
  Bucket 0: [2, 802]     (tens digit is 0)
  Bucket 4: [45]         (tens digit is 4)
  Bucket 6: [66]         (tens digit is 6)
  Bucket 7: [170, 75]    (tens digit is 7)
  Bucket 9: [90]         (tens digit is 9)
  → [2, 802, 45, 66, 170, 75, 90]

Pass 3 — hundreds digit:
  Bucket 0: [2, 45, 66, 75, 90]   (hundreds digit is 0)
  Bucket 1: [170]                  (hundreds digit is 1)
  Bucket 8: [802]                  (hundreds digit is 8)
  → [2, 45, 66, 75, 90, 170, 802]  ✓ Sorted
```

At no point was "is 170 greater than 45?" ever asked. Each pass just reads a digit and files the number.

**Complexity:**
- Time: O(d × n) where d = number of digits in the largest value, n = count of elements
- Space: O(n + 10) — the 10 buckets never grow beyond the input size combined
- Comparisons: **0**

```bash
# Sort [170, 45, 75, 90, 2, 802, 66] in 3 passes
big-oh-no digit 170 45 75 90 2 802 66

# Works with duplicates too
big-oh-no digit 3 1 4 1 5 9 2 6
```

---


## 🧬 Darwin Sort

*"It is not the strongest of the permutations that survives, nor the most sorted — but the one most adaptable to change."*

### Inspiration

In 1859, Charles Darwin published *On the Origin of Species* and changed how we understand life. His central insight was simple: organisms vary, some variations are better suited to their environment, and those organisms are more likely to reproduce. Given enough generations, this blind process of variation and selection produces complex, well-adapted creatures — all without a designer, a plan, or any awareness of the goal.

Genetic algorithms took that idea and turned it into code. John Holland formalised them in the 1970s: maintain a population of candidate solutions, score them on how close they are to the goal, let the best ones breed, introduce random mutations, and repeat. It works surprisingly well on problems where the search space is too large to brute-force and too irregular for gradient descent.

Darwin Sort applies that to a list of numbers. A population of random permutations competes for survival. Each generation, the fittest — the ones closest to sorted order — are selected to breed. Crossover mixes their genes. Mutation shakes things up. The unfit are culled. Given enough generations, natural selection converges on the sorted order. Or the species goes extinct trying. Darwin sits aboard the HMS Beagle, notebook open, watching. He doesn't intervene. He just observes, takes notes, and waits for nature to find the answer.

The algorithm is powered by [DEAP](https://github.com/deap/deap)'s `eaSimple` — the standard simple evolutionary algorithm with built-in statistics tracking, Hall of Fame, and logbook.

### The fitness function

The entire algorithm hinges on one question: given two permutations, which one is closer to sorted? The answer is adjacent-pair counting:

$$\text{fitness}(p) = \frac{|\{i : p_i \leq p_{i+1}\}|}{n - 1}$$

Walk through the permutation left to right. Every time a pair of neighbours is in the right order, that's one point. Divide by the total number of pairs to get a score between 0.0 and 1.0.

Why this works: it creates a smooth gradient. A completely reversed list scores 0.0 — every pair is wrong. A perfectly sorted list scores 1.0 — every pair is right. A mostly-wrong permutation that happens to have a few pairs in order still scores above zero, and that's enough for selection to favour it over something worse. Over many generations, the population drifts toward 1.0.

For `[3, 1, 4, 2, 5]` with 4 adjacent pairs:

| Pair | In order? |
|------|-----------|
| 3 ≤ 1 | ✗ |
| 1 ≤ 4 | ✓ |
| 4 ≤ 2 | ✗ |
| 2 ≤ 5 | ✓ |

2 out of 4 correct → fitness = **0.50**

Compare that to `[1, 3, 2, 4, 5]`:

| Pair | In order? |
|------|-----------|
| 1 ≤ 3 | ✓ |
| 3 ≤ 2 | ✗ |
| 2 ≤ 4 | ✓ |
| 4 ≤ 5 | ✓ |

3 out of 4 correct → fitness = **0.75**

Tournament selection picks the second one. That's the gradient doing its job.

### How it works

1. Generate a **population** of random permutations of the input list
2. **Score** each permutation using the fitness function above
3. **Select** the fittest individuals via tournament selection (pick 3 at random, keep the best)
4. **Crossover** — pairs of parents swap segments of their ordering to produce offspring (ordered crossover, preserving permutation validity)
5. **Mutate** — randomly shuffle a subset of positions in some offspring
6. **Elitism** — the single best individual ever seen (Hall of Fame) is always carried forward, so fitness never regresses
7. Repeat until fitness reaches 1.0 (perfectly sorted) or the generation budget runs out

### Worked example

```
Input: [5, 3, 1, 4, 2]
Population size: 50
4 adjacent pairs to get right

Gen  0: Best [3, 1, 5, 4, 2]  fitness 25%  (1/4 pairs correct)
        Avg fitness across population: ~18%
        Most individuals are random noise.

Gen  3: Best [1, 3, 2, 4, 5]  fitness 75%  (3/4 pairs correct)
        Selection has killed off the worst permutations.
        Crossover between [1,3,5,4,2] and [3,1,2,4,5] produced this.

Gen  7: Best [1, 2, 3, 4, 5]  fitness 100% (4/4 pairs correct)
        ✅ Converged. Darwin nods approvingly.
```

For 5 elements there are only 120 possible permutations. A population of 50 covers nearly half the search space on the first generation alone. Convergence is near-instant.

### How does list size affect convergence?

More elements, worse odds. The search space grows factorially — 5 elements is 120 permutations, 10 is 3.6 million, 15 is over a trillion. The default population of 50 becomes a vanishingly small sample.

Each cell is the percentage of random starting orderings that converged within 500 generations, tested across 20 trials:

| Elements | Permutations | pop=50 | pop=100 | pop=200 | Avg gens (pop=50) |
|----------|--------------|--------|---------|---------|-------------------|
| 3 | 6 | 100% | 100% | 100% | 0 |
| 5 | 120 | 100% | 100% | 100% | 20 |
| 8 | 40,320 | 40% | 65% | 90% | 339 |
| 10 | 3,628,800 | 30% | 30% | 35% | 383 |
| 15 | 1.3 trillion | 0% | 0% | 0% | 500 |

At 3–5 elements, it always converges. At 8, throwing more individuals at the problem helps — doubling from 50 to 100 nearly doubles the success rate, and 200 gets it to 90%. At 10, even quadrupling the population barely moves the needle. At 15, nothing converges within 500 generations regardless of population size.

Mutation rate matters more than population size at the margins. Higher mutation keeps the gene pool diverse and prevents premature convergence on a local optimum:

| Mutation rate | Convergence (n=10, pop=50) | Avg gens |
|---------------|----------------------------|----------|
| 0.05 | 5% | 476 |
| 0.2 | 10% | 451 |
| 0.5 | 20% | 412 |
| 0.8 | 50% | 354 |

At 80% mutation the algorithm is almost more random search than evolution — but for a 10-element list, that chaos is exactly what's needed to stumble onto the answer.

**Complexity:**
- Time: O(generations × population × n) — each generation evaluates up to `population_size` individuals, each evaluation is O(n)
- Space: O(population × n)
- Convergence: not guaranteed — the species may go extinct

Options:
- `--max-generations <n>` — generation budget before extinction (default `500`)
- `--population-size <n>` — individuals per generation (default `50`, min `2`)
- `--mutation-rate <0.0–1.0>` — probability of mutating an individual (default `0.2`)
- `--crossover-rate <0.0–1.0>` — probability of crossover between parents (default `0.7`)

```bash
big-oh-no darwin 5 3 1 4 2
big-oh-no darwin --max-generations 200 9 1 8 2 7
big-oh-no darwin --population-size 100 --mutation-rate 0.5 5 3 1 4 2
big-oh-no darwin --mutation-rate 0.05 --crossover-rate 0.9 10 9 8 7 6 5 4 3 2 1
```

---

## 📊 Implementation Status

| Algorithm | Python | Rust |
|-----------|:------:|:----:|
| Wait Sort | ✅ | 🚧 |
| Stalin Sort | ✅ | 🚧 |
| Linus Sort | ✅ | 🚧 |
| Bogo Sort | ✅ | 🚧 |
| Schrödinger Sort | ✅ | 🚧 |
| Urinal Sort | ✅ | 🚧 |
| Digit Sort | ✅ | 🚧 |
| Darwin Sort | ✅ | 🚧 |

---

## 🤝 Contribute

See [CONTRIBUTING.md](CONTRIBUTING.md) — adding a new algorithm, improving an existing one, or porting to a new language.

---

## 🙏 Acknowledgments

- **Wait Sort** — Inspired by the concept of Sleep Sort
- **Stalin Sort** — Inspired by the infamous "Stalin Sort" meme
- **Linus Sort** — Inspired by Linus Torvalds' legendary code review style on LKML
- **Bogo Sort** — Inspired by the classic bogosort thought experiment
- **Schrödinger Sort** — Inspired by the Schrödinger's cat thought experiment
- **Urinal Sort** — Inspired by the [urinal problem](https://en.wikipedia.org/wiki/Urinal_problem) and the unwritten rules of men's restroom etiquette
- **Digit Sort** — Inspired by Herman Hollerith's 1887 tabulating machines and [Radix Sort](https://en.wikipedia.org/wiki/Radix_sort); original suggestion by u/CraigAT on Reddit
- **Darwin Sort** — Inspired by Charles Darwin's theory of natural selection and [genetic algorithms](https://en.wikipedia.org/wiki/Genetic_algorithm); powered by [DEAP](https://github.com/deap/deap)


<p align="center">
  <i>Remember: Just because you can sort this way doesn't mean you should.</i>
</p>

<p align="center">
  <b>Big O(No)</b> — Where algorithms go to die... entertainingly.
</p>
