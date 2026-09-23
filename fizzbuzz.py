# fizzbuzz.py
import random
import sys
import time
import argparse

# --- 1. Target Function ---
def parse_header(data: str):
    """Target function designed to showcase progressive branch coverage."""
    if len(data) < 3:
        return  # Stage 1: Length check

    if data[0] == "F":
        # Stage 2: First magic character matched
        if data[1:3] == "UZ":
            # Stage 3: Header validated
            if len(data) > 4 and data[4] == "!":
                # Stage 4: Payload trigger reached!
                raise ValueError("CRASH DETECTED: Bug in payload handler!")


# --- 2. Mutation Operators ---
# Bias toward characters that unlock deeper target branches
_INTERESTING_CHARS = ["F", "U", "Z", "!"]
_ALL_PRINTABLE = [chr(i) for i in range(32, 127)]


def _random_char():
    """Return a random printable character, biased toward target-relevant chars."""
    if random.random() < 0.5:
        return random.choice(_INTERESTING_CHARS)
    return random.choice(_ALL_PRINTABLE)


def mutate(s: str) -> str:
    """Applies 1-4 random mutations (insert, delete, or substitute character).

    Heavier weight on insertions helps the fuzzer build up strings
    progressively, while the character bias nudges it toward the
    target payload characters.
    """
    if not s:
        return "A"

    s_list = list(s)
    # Apply 1-4 mutations per candidate for faster exploration
    for _ in range(random.randint(1, 4)):
        if not s_list:
            break
        op = random.choices(["flip", "insert", "delete"], weights=[2, 5, 1])[0]
        idx = random.randint(0, len(s_list) - 1)

        if op == "flip":
            s_list[idx] = _random_char()
        elif op == "insert":
            s_list.insert(idx, _random_char())
        elif op == "delete" and len(s_list) > 1:
            s_list.pop(idx)

    return "".join(s_list)


# --- 3. Coverage Tracker ---
class CoverageTracker:
    def __init__(self):
        self.executed_lines = set()

    def trace_func(self, frame, event, arg):
        if event == "line":
            # Track line numbers inside the target function
            if frame.f_code.co_name == "parse_header":
                self.executed_lines.add(frame.f_lineno)
        return self.trace_func


# --- 4. Fuzzing Engine & Live Demo UI ---
def run_fuzzer(max_executions: int = 10000, seed: int = None):
    if seed is not None:
        random.seed(seed)

    seed_pool = ["hello"]  # Starting seed
    global_coverage = set()
    total_executions = 0
    crashes = []

    print("=" * 60)
    print("  Fizzbuzz: Mutation-Based Fuzzing Demo")
    print("=" * 60)
    print(f"Initial Seed Pool: {seed_pool}\n")
    print("Starting Evolutionary Loop...\n")
    time.sleep(1)

    while not crashes and total_executions < max_executions:
        total_executions += 1

        # Pick a seed and mutate it
        parent_seed = random.choice(seed_pool)
        candidate_input = mutate(parent_seed)

        # Run candidate with line tracking
        tracker = CoverageTracker()
        sys.settrace(tracker.trace_func)

        crashed = False
        try:
            parse_header(candidate_input)
        except ValueError as e:
            crashed = True
            crashes.append((candidate_input, str(e)))
        finally:
            sys.settrace(None)

        # Check for newly discovered lines
        new_lines = tracker.executed_lines - global_coverage
        if new_lines:
            global_coverage.update(tracker.executed_lines)
            seed_pool.append(candidate_input)

            print(
                f"[+ COVERAGE HIT] Exec #{total_executions:<4} | "
                f"Input: {repr(candidate_input):<12} | "
                f"Total Lines Covered: {len(global_coverage)}"
            )
            time.sleep(0.1)  # Brief pause for live presentation pacing

        if crashed:
            print(
                f"\n[! CRASH DISCOVERED] Exec #{total_executions} | "
                f"Input: {repr(candidate_input)}"
            )
            break

    # --- Demo Summary ---
    print("\n" + "=" * 60)
    print("  FUZZING COMPLETE")
    print("=" * 60)
    print(f"• Total Executions : {total_executions}")
    print(f"• Final Seed Pool  : {seed_pool}")
    print(f"• Lines Covered    : {len(global_coverage)}")
    print(f"• Crashes Found    : {len(crashes)}")
    if crashes:
        print(f"• Payload Trigger  : {repr(crashes[0][0])}")


def main():
    parser = argparse.ArgumentParser(
        description="Fizzbuzz: A mutation-based fuzzing demo tool."
    )
    parser.add_argument(
        "--max-executions",
        type=int,
        default=10000,
        help="Maximum number of fuzzing executions (default: 10000)",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Random seed for reproducible fuzzing runs",
    )
    args = parser.parse_args()
    run_fuzzer(max_executions=args.max_executions, seed=args.seed)


if __name__ == "__main__":
    main()
