import sys
import json

class NQueensSolver:
    def __init__(self, n):
        self.n = n
        self.count = 0
        self.nodes_visited = 0  # Novo contador
        # Helper arrays for O(1) checks
        self.cols = [False] * n
        self.left_diag = [False] * (2 * n - 1)
        self.right_diag = [False] * (2 * n - 1)

    def solve(self, row):
        """Recursive backtracking function"""
        self.nodes_visited += 1 # Rastreia cada chamada de 'solve'

        if row == self.n:
            self.count += 1
            return

        for col in range(self.n):
            # Check if the current spot is safe
            if (not self.cols[col] and
                not self.left_diag[row + col] and
                not self.right_diag[row - col + self.n - 1]):
                
                # Place queen
                self.cols[col] = True
                self.left_diag[row + col] = True
                self.right_diag[row - col + self.n - 1] = True
                
                # Recurse to the next row
                self.solve(row + 1)
                
                # Backtrack: remove queen
                self.cols[col] = False
                self.left_diag[row + col] = False
                self.right_diag[row - col + self.n - 1] = False

    def get_total_solutions(self):
        self.solve(0)
        return self.count

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 n_queens.py <N>", file=sys.stderr)
        sys.exit(1)

    try:
        n = int(sys.argv[1])
        if n <= 0:
            raise ValueError()
    except ValueError:
        print("Error: <N> must be a positive integer.", file=sys.stderr)
        sys.exit(1)

    solver = NQueensSolver(n)
    total_solutions = solver.get_total_solutions()
    
    # Nova saída JSON
    output = {
        "solutions": total_solutions,
        "nodes_visited": solver.nodes_visited
    }
    print(json.dumps(output))