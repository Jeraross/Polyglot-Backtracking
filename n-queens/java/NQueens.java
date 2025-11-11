public class NQueens {

    private final int n;
    private long count; // Usar 'long' para evitar estouro
    private long nodes_visited; // Novo contador
    private final boolean[] cols;
    private final boolean[] leftDiags;
    private final boolean[] rightDiags;

    public NQueens(int n) {
        this.n = n;
        this.count = 0;
        this.nodes_visited = 0; // Inicializa o contador
        this.cols = new boolean[n];
        this.leftDiags = new boolean[2 * n - 1];
        this.rightDiags = new boolean[2 * n - 1];
    }

    private void solve(int row) {
        this.nodes_visited++; // Rastreia cada chamada

        if (row == n) {
            count++;
            return;
        }

        for (int col = 0; col < n; col++) {
            // Calculate diagonal indices
            int leftDiagIdx = row + col;
            int rightDiagIdx = row - col + n - 1;

            // Check if safe
            if (!cols[col] && !leftDiags[leftDiagIdx] && !rightDiags[rightDiagIdx]) {
                // Place queen
                cols[col] = true;
                leftDiags[leftDiagIdx] = true;
                rightDiags[rightDiagIdx] = true;

                // Recurse
                solve(row + 1);

                // Backtrack
                cols[col] = false;
                leftDiags[leftDiagIdx] = false;
                rightDiags[rightDiagIdx] = false;
            }
        }
    }

    public long getTotalSolutions() {
        solve(0); // Start the recursive process from row 0
        return count;
    }

    // Adiciona um getter para o contador de nós
    public long getNodesVisited() {
        return nodes_visited;
    }

    public static void main(String[] args) {
        if (args.length != 1) {
            System.err.println("Usage: java NQueens <N>");
            System.exit(1);
        }

        int n = 0;
        try {
            n = Integer.parseInt(args[0]);
            if (n <= 0) {
                throw new NumberFormatException();
            }
        } catch (NumberFormatException e) {
            System.err.println("Error: <N> must be a positive integer.");
            System.exit(1);
        }

        NQueens problem = new NQueens(n);
        long total_solutions = problem.getTotalSolutions();
        long total_nodes = problem.getNodesVisited();

        // Nova saída JSON (formatada manualmente para evitar dependências)
        System.out.println(String.format(
            "{\"solutions\": %d, \"nodes_visited\": %d}",
            total_solutions,
            total_nodes
        ));
    }
}