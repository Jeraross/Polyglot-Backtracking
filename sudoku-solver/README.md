# Sudoku Solver

This directory contains polyglot implementations of a backtracking algorithm to solve 9x9 **Sudoku** puzzles.

The algorithm attempts to fill empty cells (usually marked with '0' or '.') one by one, checking if the new digit violates any Sudoku rules (row, column, or 3x3 subgrid). If a choice leads to a dead end, it backtracks.

## Implementations

* **Python (`./python/`):** A standard recursive implementation.
* **C++ (`./cpp/`):** A performance-focused implementation.
* **Haskell (`./haskell/`):** A functional approach to solving the grid.
* **Assembly (`./assembly/`):** A low-level implementation.

## Input File Format

All programs expect a text file as a command-line argument. This file must represent the 9x9 Sudoku board.

* Use digits `1` through `9` for pre-filled cells.
* Use `0` or `.` for empty cells.
* The file must contain 9 lines, each with 9 characters.

An example (`sample_board.txt`) is included:

530070000 600195000 098000060 800060003 400803001 700020006 060000280 000419005 000080079


## How to Run

All commands should be run from this directory (e.g., `Polyglot-Backtracking/sudoku-solver/`). The programs will read the input file and print the solved board.

### Python

```bash
# Usage: python3 ./python/sudoku.py <input_file>
# Example:
python3 ./python/sudoku.py ./sample_board.txt
```

### C++

A Makefile is provided in the cpp/ directory.

```bash
# 1. Compile (using Makefile):
(cd cpp && make)

# 1b. Compile (manually with g++):
# g++ -o ./cpp/sudoku ./cpp/sudoku.cpp -O2

# 2. Run:
# Usage: ./cpp/sudoku <input_file>
# Example:
./cpp/sudoku ./sample_board.txt
```

### Haskell

The Haskell implementation must be compiled first using GHC.

```bash

# 1. Compile (with optimizations):
ghc -o ./haskell/sudoku ./haskell/Sudoku.hs -O2

# 2. Run:
# Usage: ./haskell/sudoku <input_file>
# Example:
./haskell/sudoku ./sample_board.txt
```

### Assembly
A Makefile is provided in the assembly/ directory.

```bash
# 1. Compile (using Makefile):
(cd assembly && make)

# 2. Run:
# Usage: ./assembly/sudoku <input_file>
# Example:
./assembly/sudoku ./sample_board.txt
```