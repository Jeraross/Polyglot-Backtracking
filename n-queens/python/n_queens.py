import sys
import json

class NQueensSolver:
    def __init__(self, n):
        self.n = n
        self.count = 0
        self.nodes_visited = 0
        self.backtracks = 0  # Novo
        self.pruned_paths = 0 # Novo
        
        self.cols = [False] * n
        self.left_diag = [False] * (2 * n - 1)
        self.right_diag = [False] * (2 * n - 1)

    def solve(self, row):
        """Recursive backtracking function"""
        self.nodes_visited += 1

        if row == self.n:
            self.count += 1
            return

        for col in range(self.n):
            if (not self.cols[col] and
                not self.left_diag[row + col] and
                not self.right_diag[row - col + self.n - 1]):
                
                # 1. Place
                self.cols[col] = True
                self.left_diag[row + col] = True
                self.right_diag[row - col + self.n - 1] = True
                
                # 2. Recurse
                self.solve(row + 1)
                
                # 3. Backtrack (recuo)
                self.backtracks += 1
                self.cols[col] = False
                self.left_diag[row + col] = False
                self.right_diag[row - col + self.n - 1] = False
            
            else:
                # 4. Pruned (podado)
                self.pruned_paths += 1

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
    
    # Saída JSON completa
    output = {
        "solutions": total_solutions,
        "nodes_visited": solver.nodes_visited,
        "backtracks": solver.backtracks,
        "pruned_paths": solver.pruned_paths
    }
    print(json.dumps(output))