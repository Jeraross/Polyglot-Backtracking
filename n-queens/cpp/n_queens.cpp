#include <iostream>
#include <vector>
#include <string>

// 'nodes_visited' é agora passado por referência para ser contado
long long solve(int row, int n, 
              std::vector<bool>& cols, 
              std::vector<bool>& left_diag, 
              std::vector<bool>& right_diag,
              long long& nodes_visited) { // Novo parâmetro
    
    nodes_visited++; // Rastreia cada chamada

    if (row == n) {
        return 1; // Found one valid solution
    }

    long long count = 0;
    for (int col = 0; col < n; ++col) {
        // Calculate diagonal indices
        int left_diag_idx = row + col;
        int right_diag_idx = row - col + n - 1;

        // Check if the spot is safe
        if (!cols[col] && !left_diag[left_diag_idx] && !right_diag[right_diag_idx]) {
            // Place queen
            cols[col] = true;
            left_diag[left_diag_idx] = true;
            right_diag[right_diag_idx] = true;

            // Recurse
            count += solve(row + 1, n, cols, left_diag, right_diag, nodes_visited);

            // Backtrack
            cols[col] = false;
            left_diag[left_diag_idx] = false;
            right_diag[right_diag_idx] = false;
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
    long long nodes_visited = 0; // Inicializa o contador

    long long total_solutions = solve(0, n, cols, left_diag, right_diag, nodes_visited);
    
    // Nova saída JSON (formatada manualmente)
    std::cout << "{\"solutions\": " << total_solutions 
              << ", \"nodes_visited\": " << nodes_visited << "}" 
              << std::endl;

    return 0;
}