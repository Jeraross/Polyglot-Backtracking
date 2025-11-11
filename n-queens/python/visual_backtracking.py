import time
import os

# --- Configurações da Visualização ---
# Use N=4 ou N=5. N=8 é muito lento para assistir!
N = 4
# Atraso em segundos (0.5 = meio segundo). Ajuste como quiser.
DELAY = 1.0
# -----------------------------------

def clear_screen():
    """Limpa a tela do terminal."""
    # 'nt' é para Windows, 'posix' (o resto) é para Linux/Mac/WSL
    os.system('cls' if os.name == 'nt' else 'clear')

class VisualNQueensSolver:
    def __init__(self, n, delay):
        self.n = n
        self.delay = delay
        self.solutions = 0
        # O tabuleiro é uma lista. board[linha] = coluna
        # -1 significa que nenhuma rainha foi colocada naquela linha.
        self.board = [-1] * n

    def print_board(self, status_message):
        """Imprime o tabuleiro atual e uma mensagem de status."""
        clear_screen()
        print(f"--- Visualizador de Backtracking N-Queens (N={self.n}) ---")
        print(f"\nStatus: {status_message}\n")
        
        for row in range(self.n):
            line = "  "
            for col in range(self.n):
                if self.board[row] == col:
                    # [Q] indica a rainha na linha atual
                    # Q   indica uma rainha colocada em uma linha anterior
                    line += "[Q] " if row == self.n - 1 or self.board[row+1] == -1 else " Q  "
                else:
                    line += " .  "
            print(line)
        
        print(f"\nSoluções encontradas: {self.solutions}")
        time.sleep(self.delay)

    def is_safe(self, row, col):
        """
        Verifica se é seguro colocar uma rainha na (linha, coluna).
        Só precisamos checar as linhas *acima* da linha atual.
        """
        for r in range(row):
            # 1. Checa a coluna:
            if self.board[r] == col:
                return False
            # 2. Checa a diagonal:
            if abs(self.board[r] - col) == abs(r - row):
                return False
        return True

    def solve(self, row):
        """A função recursiva de backtracking."""
        
        # --- Caso Base: Solução Encontrada ---
        if row == self.n:
            self.solutions += 1
            self.print_board(f"SOLUÇÃO {self.solutions} ENCONTRADA! (Pressione Enter)")
            input() # Pausa até o usuário pressionar Enter
            return

        # --- Caso Recursivo: Tentar todas as colunas nesta linha ---
        for col in range(self.n):
            
            # 1. VERIFICAR: É seguro colocar aqui?
            if self.is_safe(row, col):
                
                # 2. ESCOLHER: Coloca a rainha
                self.board[row] = col
                self.print_board(f"Colocando em (Linha {row}, Col {col})")
                
                # 3. EXPLORAR: Chama a recursão para a próxima linha
                self.solve(row + 1)
                
                # 4. DESFAZER (O BACKTRACK VISÍVEL!)
                # Se voltamos de solve(row+1), exploramos todo esse caminho.
                # Devemos remover a rainha para tentar a próxima coluna.
                self.board[row] = -1
                self.print_board(f"BACKTRACK: Removendo de (Linha {row}, Col {col})")
            
            # Se não for seguro (else), o loop 'for' simplesmente
            # continua para a próxima coluna, o que é um "mini-backtrack".

# --- Execução Principal ---
if __name__ == "__main__":
    solver = VisualNQueensSolver(N, DELAY)
    try:
        solver.solve(0)
        clear_screen()
        print(f"Visualização concluída. Total de {solver.solutions} soluções encontradas para N={N}.")
    except KeyboardInterrupt:
        clear_screen()
        print("\nVisualização interrompida pelo usuário.")