#include <iostream>
#include <string>

long long count = 0;
long long nodes_visited = 0; // Novo contador global
long long ALL_SET = 0; 

void solve(long long col, long long ld, long long rd) {
    nodes_visited++; // Rastreia cada chamada

    if (col == ALL_SET) {
        count++;
        return;
    }

    long long possible = ~(col | ld | rd) & ALL_SET;

    while (possible) {
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

    int n;
    try {
        n = std::stoi(argv[1]);
        if (n <= 0 || n > 63) {
             throw std::invalid_argument("N must be between 1 and 63");
        }
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }

    ALL_SET = (1LL << n) - 1;

    solve(0, 0, 0);

    // Nova saída JSON (formatada manualmente)
    std::cout << "{\"solutions\": " << count 
              << ", \"nodes_visited\": " << nodes_visited << "}" 
              << std::endl;

    return 0;
}