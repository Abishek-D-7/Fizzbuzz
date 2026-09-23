# Fizzbuzz

A minimal, self-contained mutation-based fuzzing demonstration tool. Fizzbuzz progressively discovers deeper branches in a target function using coverage-guided seed evolution.

## Quick Start

```bash
python fizzbuzz.py
```

## Optional Flags

- `--max-executions N` – Stop after N fuzzing iterations (default: 10000).
- `--seed S` – Set a random seed for reproducible demos. For example, `--seed 42`.

## How It Works

Fizzbuzz uses a **coverage-guided evolutionary fuzzing** loop to progressively unlock deeper branches in a staged target function.

### 1. Target Function
The `parse_header(data)` function has four nested stages:
- **Stage 1**: Input length must be at least 3 characters.
- **Stage 2**: First character must be `F`.
- **Stage 3**: Second and third characters must be `UZ`.
- **Stage 4**: A fifth character must exist and be `!` to trigger the crash.

### 2. Mutation Engine
Each fuzzing iteration picks a seed from the current pool and applies 1–4 random mutations:
- **Flip** — replace a character with a random printable character.
- **Insert** — add a random printable character at a random position (weighted heavily).
- **Delete** — remove a character at a random position.

The mutation engine is **biased** toward the payload-relevant characters (`F`, `U`, `Z`, `!`) to keep the demo reliable and fast.

### 3. Coverage Tracker
`sys.settrace` is used to record every line executed inside `parse_header`. After each run, the fuzzer checks whether any **new** lines were discovered.

### 4. Seed Pool Evolution
If a mutated input reaches a line that was never executed before, that input is saved into the **seed pool**. This means future mutations will build upon inputs that have already proven they can reach deeper branches. Over time, the fuzzer progresses from simple length checks all the way to the crash payload.

### 5. Crash Discovery
When an input satisfies all four stages, `parse_header` raises a `ValueError`. The fuzzer immediately stops, reports the execution count, and prints the exact payload that triggered the bug.

## Sample Run

Here is an annotated example of what you will see when you run the tool:

```bash
$ python fizzbuzz.py --seed 42
```

```
[+ COVERAGE HIT] Exec #1    | Input: 'hFello'     | Total Lines Covered: 2
```
> The first mutated input passes the length check and discovers a new line. It is saved to the seed pool.

```
[+ COVERAGE HIT] Exec #37   | Input: 'FU!ello'    | Total Lines Covered: 3
```
> A seed from the pool is mutated again. By chance the first character becomes `F`, unlocking Stage 2. The seed pool grows.

```
[+ COVERAGE HIT] Exec #58   | Input: 'FUZ!-lZlo'  | Total Lines Covered: 4
```
> Further mutations hit the `UZ` header check (Stage 3). The fuzzer is now guided toward the final payload.

```
[+ COVERAGE HIT] Exec #80   | Input: 'FUZ=!-U!lZlo' | Total Lines Covered: 5
```
> The input grows long enough to reach the fifth character position.

```
[! CRASH DISCOVERED] Exec #80 | Input: 'FUZ=!-U!lZlo'
```
> Stage 4 is satisfied (`data[4] == '!'`) and the bug is triggered. The demo stops and prints the complete summary.

### Summary Output
```
FUZZING COMPLETE
• Total Executions : 80
• Final Seed Pool  : ['hello', 'hFello', 'FU!ello', 'FUZ!-lZlo', 'FUZ=!-U!lZlo']
• Lines Covered    : 5
• Crashes Found    : 1
• Payload Trigger  : 'FUZ=!-U!lZlo'
```

## What It Demonstrates

1. **Mutation Engine** – Random insert, delete, or character-flip mutations on seed inputs.
2. **Coverage Tracking** – Uses `sys.settrace` to record which lines inside `parse_header` are executed.
3. **Seed Pool Evolution** – Any input that hits a new line is added to the seed pool, guiding the fuzzer deeper into nested branches stage-by-stage.
4. **Crash Discovery** – When the fuzzer reaches the final payload condition, it triggers a `ValueError` and reports the crashing input.
