#include <iostream>
#include <string>

long long count = 0;
long long nodes_visited = 0;     // Chamadas para solve() - uma por linha
long long explored_placements = 0; // Número de chamadas recursivas (bits '1' em 'possible')
long long pruned_paths = 0;      // Número de bits '0' em 'possible'
long long ALL_SET = 0; 
int BOARD_SIZE = 0; // Precisamos de N

// Função para contar bits '1' (popcount) se __builtin não estiver disponível
int popcount(long long x) {
    int count = 0;
    while (x) {
        x &= (x - 1);
        count++;
    }
    return count;
}

void solve(long long col, long long ld, long long rd) {
    nodes_visited++; 

    if (col == ALL_SET) {
        count++;
        return;
    }

    long long possible = ~(col | ld | rd) & ALL_SET;
    
    // Popcount de GCC é mais rápido, mas manual funciona
    // int ones = __builtin_popcountll(possible);
    // int zeros = BOARD_SIZE - ones;
    int ones = popcount(possible);
    int zeros = BOARD_SIZE - ones;

    pruned_paths += zeros;

    while (possible) {
        explored_placements++; // Contando cada colocação real explorada
        long long bit = possible & -possible;
        possible -= bit;
        solve(col | bit, (ld | bit) << 1, (rd | bit) >> 1);
    }
}

int main(int argc, char* argv[]) {
    if (argc != 2) {
        std::cerr << "Usage: ./n_queens_bitboard <N>" << std::endl;
        return 1;
    }

    try {
        BOARD_SIZE = std::stoi(argv[1]); // Salva N globalmente
        if (BOARD_SIZE <= 0 || BOARD_SIZE > 63) {
             throw std::invalid_argument("N must be between 1 and 63");
        }
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }

    ALL_SET = (1LL << BOARD_SIZE) - 1;

    solve(0, 0, 0);

    // Saída JSON completa
    std::cout << "{\"solutions\": " << count 
              << ", \"nodes_visited\": " << nodes_visited 
              << ", \"explored_placements\": " << explored_placements
              << ", \"pruned_paths\": " << pruned_paths
              << "}" << std::endl;

    return 0;
}