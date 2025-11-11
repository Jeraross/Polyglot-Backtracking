#include <iostream>
#include <vector>
#include <string>

// 'nodes_visited', 'backtracks', e 'pruned_paths' são passados por referência
long long solve(int row, int n, 
              std::vector<bool>& cols, 
              std::vector<bool>& left_diag, 
              std::vector<bool>& right_diag,
              long long& nodes_visited,
              long long& backtracks,
              long long& pruned_paths) {
    
    nodes_visited++; 

    if (row == n) {
        return 1; // Achou uma solução
    }

    long long count = 0;
    for (int col = 0; col < n; ++col) {
        int left_diag_idx = row + col;
        int right_diag_idx = row - col + n - 1;

        // Se for seguro, explore
        if (!cols[col] && !left_diag[left_diag_idx] && !right_diag[right_diag_idx]) {
            // 1. Coloca a rainha
            cols[col] = true;
            left_diag[left_diag_idx] = true;
            right_diag[right_diag_idx] = true;

            // 2. Recurse
            count += solve(row + 1, n, cols, left_diag, right_diag, nodes_visited, backtracks, pruned_paths);

            // 3. Backtrack (recuo)
            // Esta é a contagem de "desfazer"
            backtracks++; 
            cols[col] = false;
            left_diag[left_diag_idx] = false;
            right_diag[right_diag_idx] = false;
        } else {
            // 4. Pruned (podado)
            // Não foi seguro, então nem tentamos.
            pruned_paths++;
        }
    }
    return count;
}

int main(int argc, char* argv[]) {
    if (argc != 2) {
        std::cerr << "Usage: ./n_queens <N>" << std::endl;
        return 1;
    }

    int n;
    try {
        n = std::stoi(argv[1]);
        if (n <= 0) throw std::invalid_argument("N must be positive");
    } catch (const std::exception& e) {
        std::cerr << "Error: <N> must be a positive integer." << std::endl;
        return 1;
    }

    std::vector<bool> cols(n, false);
    std::vector<bool> left_diag(2 * n - 1, false);
    std::vector<bool> right_diag(2 * n - 1, false);
    
    long long nodes_visited = 0;
    long long backtracks = 0;
    long long pruned_paths = 0;

    long long total_solutions = solve(0, n, cols, left_diag, right_diag, nodes_visited, backtracks, pruned_paths);
    
    // Saída JSON completa
    std::cout << "{\"solutions\": " << total_solutions 
              << ", \"nodes_visited\": " << nodes_visited 
              << ", \"backtracks\": " << backtracks
              << ", \"pruned_paths\": " << pruned_paths
              << "}" << std::endl;

    return 0;
}