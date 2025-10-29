# N-Queens Problem

This directory contains polyglot implementations for solving the **N-Queens Problem**.

The problem is to place `N` chess queens on an `N×N` chessboard so that no two queens threaten each other. This means no two queens can share the same row, column, or diagonal.

## Implementations

* **Python (`./python/`):** A clear, recursive backtracking solution.
* **C++ (`./cpp/`):**
    * `n_queens.cpp`: A standard recursive backtracking solution, similar to the Python one.
    * `n_queens_bitboard.cpp`: (Optional, as discussed) A highly optimized version using bit manipulation (bitboards) to check for attacks in O(1) time.
* **Haskell (`./haskell/`):** A declarative, functional solution that elegantly describes the properties of a valid solution.
* **Assembly (`./assembly/`):** A low-level implementation for performance baseline.

## How to Run

All commands should be run from this directory (e.g., `Polyglot-Backtracking/n-queens/`). The programs will print the total number of valid solutions found.

### Python

The Python script takes `N` (the board size) as a command-line argument.

```bash
# Usage: python3 ./python/n_queens.py <N>
# Example for N=8:
python3 ./python/n_queens.py 8
```

### C++

A Makefile is provided in the cpp/ directory for convenience.

```bash
# 1. Compile (using Makefile):
(cd cpp && make)

# 1b. Compile (manually with g++):
# g++ -o ./cpp/n_queens ./cpp/n_queens.cpp -O2
# g++ -o ./cpp/n_queens_bitboard ./cpp/n_queens_bitboard.cpp -O2

# 2. Run:
# Usage: ./cpp/n_queens <N>
# Example for N=8:
./cpp/n_queens 8

# Example for the bitboard version (N=14):
./cpp/n_queens_bitboard 14
```

### Haskell

The Haskell implementation must be compiled first using GHC.

```bash
# 1. Compile (with optimizations):
ghc -o ./haskell/n_queens ./haskell/NQueens.hs -O2

# 2. Run:
# Usage: ./haskell/n_queens <N>
# Example for N=8:
./haskell/n_queens 8
```

### Assembly

A Makefile is provided in the assembly/ directory. This assumes nasm and ld are installed.

```bash
# 1. Compile (using Makefile):
(cd assembly && make)

# 1b. Compile (manually 64-bit Linux):
# nasm -f elf64 -o ./assembly/n_queens.o ./assembly/n_queens.asm
# ld -o ./assembly/n_queens ./assembly/n_queens.o

# 2. Run:
# Note: Assembly implementations may have N hardcoded
# or expect it in a specific register. Check the .asm file.
# If it supports command-line args (complex in asm), it would be:
./assembly/n_queens 8
```