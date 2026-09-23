# Fizzbuzz

A minimal, self-contained mutation-based fuzzing demonstration tool. Fizzbuzz progressively discovers deeper branches in a target function using coverage-guided seed evolution.

## Quick Start

```bash
python fizzbuzz.py
```

## Optional Flags

- `--max-executions N` – Stop after N fuzzing iterations (default: 10000).
- `--seed S` – Set a random seed for reproducible demos. For example, `--seed 42`.

## What It Demonstrates

1. **Mutation Engine** – Random insert, delete, or character-flip mutations on seed inputs.
2. **Coverage Tracking** – Uses `sys.settrace` to record which lines inside `parse_header` are executed.
3. **Seed Pool Evolution** – Any input that hits a new line is added to the seed pool, guiding the fuzzer deeper into nested branches stage-by-stage.
4. **Crash Discovery** – When the fuzzer reaches the final payload condition, it triggers a `ValueError` and reports the crashing input.
