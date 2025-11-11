# Compiler and flags
CXX = g++
CXXFLAGS = -std=c++17 -O2 -Wall

# Executable names
TARGETS = n_queens n_queens_bitboard

# Default rule
all: $(TARGETS)

# Rule for the standard N-Queens
n_queens: n_queens.cpp
	$(CXX) $(CXXFLAGS) -o $@ $^

# Rule for the bitboard N-Queens
n_queens_bitboard: n_queens_bitboard.cpp
	$(CXX) $(CXXFLAGS) -o $@ $^

# Clean rule
clean:
	rm -f $(TARGETS)

.PHONY: all clean