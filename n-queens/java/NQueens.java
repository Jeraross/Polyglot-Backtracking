public class NQueens {

    private final int n;
    private long count;
    private long nodes_visited;
    private long backtracks; // Novo
    private long pruned_paths; // Novo
    private final boolean[] cols;
    private final boolean[] leftDiags;
    private final boolean[] rightDiags;

    public NQueens(int n) {
        this.n = n;
        this.count = 0;
        this.nodes_visited = 0;
        this.backtracks = 0;
        this.pruned_paths = 0;
        this.cols = new boolean[n];
        this.leftDiags = new boolean[2 * n - 1];
        this.rightDiags = new boolean[2 * n - 1];
    }

    private void solve(int row) {
        this.nodes_visited++;

        if (row == n) {
            count++;
            return;
        }

        for (int col = 0; col < n; col++) {
            int leftDiagIdx = row + col;
            int rightDiagIdx = row - col + n - 1;

            if (!cols[col] && !leftDiags[leftDiagIdx] && !rightDiags[rightDiagIdx]) {
                // 1. Place
                cols[col] = true;
                leftDiags[leftDiagIdx] = true;
                rightDiags[rightDiagIdx] = true;

                // 2. Recurse
                solve(row + 1);

                // 3. Backtrack (recuo)
                this.backtracks++;
                cols[col] = false;
                leftDiags[leftDiagIdx] = false;
                rightDiags[rightDiagIdx] = false;
            } else {
                // 4. Pruned (podado)
                this.pruned_paths++;
            }
        }
    }

    public long getTotalSolutions() {
        solve(0);
        return count;
    }
    
    // Getters para os novos dados
    public long getNodesVisited() { return nodes_visited; }
    public long getBacktracks() { return backtracks; }
    public long getPrunedPaths() { return pruned_paths; }

    public static void main(String[] args) {
        if (args.length != 1) {
            System.err.println("Usage: java NQueens <N>");
            System.exit(1);
        }

        int n = 0;
        try {
            n = Integer.parseInt(args[0]);
            if (n <= 0) { throw new NumberFormatException(); }
        } catch (NumberFormatException e) {
            System.err.println("Error: <N> must be a positive integer.");
            System.exit(1);
        }

        NQueens problem = new NQueens(n);
        long total_solutions = problem.getTotalSolutions();
        
        // Coleta todos os dados
        long total_nodes = problem.getNodesVisited();
        long total_backtracks = problem.getBacktracks();
        long total_pruned = problem.getPrunedPaths();

        // Saída JSON completa
        System.out.println(String.format(
            "{\"solutions\": %d, \"nodes_visited\": %d, \"backtracks\": %d, \"pruned_paths\": %d}",
            total_solutions, total_nodes, total_backtracks, total_pruned
        ));
    }
}