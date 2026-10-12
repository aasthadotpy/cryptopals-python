# Cryptopals in Python

My progress through the [Cryptopals cryptography challenges](https://cryptopals.com/).
I keep solutions, tests, and short notes here as I work through each challenge.

## Setup

Use Python 3.10 or newer. No third-party runtime dependencies are needed yet.

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Run tests from the repository root:

```bash
python3 -m unittest discover -s tests -v
```

The initial tests are skipped until I implement the corresponding challenges.
Remove each skip decorator when its solution is ready.

## Layout

- `cryptopals/set01/`: solution modules for set 1.
- `cryptopals/utils.py`: helpers shared between challenges, added as needed.
- `tests/`: standard-library `unittest` tests.
- `notes/set01.md`: approaches, mistakes, and lessons learned.

## Progress

### Set 1

- [ ] Challenge 1
- [ ] Challenge 2
- [ ] Challenge 3
- [ ] Challenge 4
- [ ] Challenge 5
- [ ] Challenge 6
- [ ] Challenge 7
- [ ] Challenge 8

Add further sets as I reach them. Check off a challenge once its solution and tests pass.

## Workflow

1. Read the challenge and implement a solution.
2. Add tests for the supplied example and useful edge cases.
3. Write a short note about the approach and what I learned.
4. Update the progress checklist and commit the completed challenge.

Example commit message: `Solve set 1 challenge 1: hex to base64`.

These implementations are learning exercises and are not intended for production security.
