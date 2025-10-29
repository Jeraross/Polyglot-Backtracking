# Polyglot-Backtracking

A repository for exploring and analyzing **backtracking** algorithms across multiple programming languages.

This project is a requirement for a **Theory of Computation** course. The primary goal is to compare implementations based on three main axes:

1.  **Performance:** Execution time and memory usage.
2.  **Expressiveness:** Readability, clarity, and lines of code.
3.  **Paradigm:** The idiomatic approach for each language (imperative, functional, etc.).

---

## Project Structure

The repository is organized by problem, with each directory containing implementations in the languages listed below.

### Classic Problems
* **`n-queens/`**: The classic N-Queens placement problem.
* **`sudoku-solver/`**: A backtracking-based Sudoku grid solver.

### Special Case: The Metroid Analogy
* **`metroid/`**: This is a conceptual implementation of the backtracking analogy, not a standard combinatorial problem. See the dedicated section below.

---

## The Languages ("The Polyglots")

Languages were chosen to highlight differences in paradigm and performance:

* **Python (High-Level):** Focus on clarity and speed of implementation.
* **C++ (Compiled):** Focus on raw performance and low-level optimization.
* **Haskell (Functional):** Focus on a declarative, immutable approach.
* **Assembly (Machine-Level):** The definitive baseline for performance, demonstrating the cost of abstraction.

---

## Special Case: The Metroid Analogy

**Why Metroid?** We use the *Metroidvania* genre as the primary analogy for backtracking's "intelligent trial-and-error" logic:

* **The Goal:** Samus (the algorithm) explores a map (the search space).
* **The Attempt:** She chooses a path (a recursive choice).
* **The Dead End:** She hits a red door without missiles (a violated constraint).
* **The "Backtrack":** She returns to the last junction (unwinds the stack) and tries the *other* path.
* **The State Change:** She finds a power-up (e.g., Morph Ball), which changes her state and validates previously invalid paths.

The code in the `/metroid` folder simulates this map exploration process as a practical, visual study of the core backtracking logic.

---

## How to Use

Each problem directory (e.g., `n-queens/`) contains its own `README.md` with specific build and execution instructions.

### General Requirements:
* C++ compiler (g++, clang)
* Python 3 interpreter
* GHC (for Haskell)
* NASM / ld (for Assembly)

Benchmark scripts and performance results can be found in the `/analysis` directory.