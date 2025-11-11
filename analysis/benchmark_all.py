import subprocess
import time
import os
import csv
import json
import resource # Para medir o uso de memória (funciona no Linux/WSL)

# --- Configuration ---
NUM_RUNS = 15  # Número de execuções para cada N e implementação
N_VALUES_STANDARD = range(4, 15) 
N_VALUES_BITBOARD = range(4, 19) 

# Paths (relative to this script's location)
PROJECT_ROOT = ".."
N_QUEENS_DIR = os.path.join(PROJECT_ROOT, "n-queens")
CPP_DIR = os.path.join(N_QUEENS_DIR, "cpp")
PY_DIR = os.path.join(N_QUEENS_DIR, "python")
JAVA_DIR = os.path.join(N_QUEENS_DIR, "java")

# --- Commands ---
COMMANDS = {
    "Python": {
        "cmd": ["python3", os.path.join(PY_DIR, "n_queens.py"), "N"],
        "impl": "Standard",
        "n_values": N_VALUES_STANDARD
    },
    "C++ (Standard)": {
        "cmd": [os.path.join(CPP_DIR, "n_queens"), "N"],
        "impl": "Standard",
        "n_values": N_VALUES_STANDARD
    },
    "Java": {
        "cmd": ["java", "-cp", JAVA_DIR, "NQueens", "N"],
        "impl": "Standard",
        "n_values": N_VALUES_STANDARD
    },
    "C++ (Bitboard)": {
        "cmd": [os.path.join(CPP_DIR, "n_queens_bitboard"), "N"],
        "impl": "Bitboard",
        "n_values": N_VALUES_BITBOARD
    }
}

def compile_sources():
    """Compile C++ and Java sources."""
    print("--- Compiling all sources ---")
    
    # Compile C++
    try:
        # Limpa builds antigos e constrói
        print("  Cleaning C++ build...")
        subprocess.run(["make", "clean"], cwd=CPP_DIR, check=True, capture_output=True, text=True)
        print("  Building C++...")
        subprocess.run(["make"], cwd=CPP_DIR, check=True, capture_output=True, text=True)
        print("C++ compiled successfully.")
    
    except FileNotFoundError as e:
        print("\n[ERRO FATAL NA COMPILAÇÃO C++]")
        print(f"  Comando 'make' ou diretório não encontrado.")
        print(f"  O script tentou rodar 'make' dentro da pasta: {CPP_DIR}")
        print(f"  Erro do sistema: {e.strerror} (No such file or directory)")
        print(f"  Verifique se o diretório '{CPP_DIR}' existe e se 'make' está instalado.")
        return False
    
    except subprocess.CalledProcessError as e:
        print("\n[ERRO FATAL NA COMPILAÇÃO C++]")
        print(f"  O comando 'make' falhou (retornou um erro).")
        print(f"  STDERR: {e.stderr}")
        return False
    
    except Exception as e:
        print(f"\n[ERRO INESPERADO NA COMPILAÇÃO C++]: {e}")
        return False

    # Compile Java
    try:
        java_file = os.path.join(JAVA_DIR, "NQueens.java")
        print(f"  Compiling Java ({java_file})...")
        # Força a recompilação
        subprocess.run(["javac", "-g", java_file], check=True, capture_output=True, text=True)
        print("Java compiled successfully.")
    
    except FileNotFoundError as e:
        print("\n[ERRO FATAL NA COMPILAÇÃO JAVA]")
        print(f"  Comando 'javac' ou arquivo/diretório não encontrado.")
        print(f"  O script tentou rodar 'javac' no arquivo: {java_file}")
        print(f"  Erro do sistema: {e.strerror} (No such file or directory)")
        print(f"  Verifique se 'javac' está instalado e se o arquivo '{java_file}' existe.")
        return False
    
    except subprocess.CalledProcessError as e:
        print("\n[ERRO FATAL NA COMPILAÇÃO JAVA]")
        print(f"  O comando 'javac' falhou (retornou um erro).")
        print(f"  STDERR: {e.stderr}")
        return False
    
    except Exception as e:
        print(f"\n[ERRO INESPERADO NA COMPILAÇÃO JAVA]: {e}")
        return False
        
    print("--- Compilation complete ---")
    return True

def run_benchmark(lang, config, n_val):
    """Runs a single benchmark and returns results."""
    cmd = [str(n_val) if item == "N" else item for item in config["cmd"]]
    
    try:
        # Reseta o uso de recursos
        # Captura o uso de memória ANTES da execução para calcular o DELTA
        mem_before = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
        
        start_time = time.perf_counter()
        
        proc = subprocess.run(
            cmd, 
            check=True, 
            capture_output=True, 
            text=True, 
            timeout=300 # Timeout de 5 minutos
        )
        
        end_time = time.perf_counter()
        
        # ru_maxrss é o PICO de uso de memória. 
        # Subtrair o 'antes' nos dá uma ideia do delta, mas o RSS total é mais robusto.
        mem_after = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
        mem_usage_kb = mem_after - mem_before
        # Vamos usar o pico total (RSS), é uma métrica mais estável do que o delta.
        mem_usage_kb_total = mem_after 

        time_taken = end_time - start_time
        
        # Analisa a nova saída JSON
        try:
            output_data = json.loads(proc.stdout.strip())
        except json.JSONDecodeError:
            print(f"    Error: Could not parse JSON output from {lang}")
            print(f"    STDOUT: {proc.stdout}")
            return None

        # Cria o dicionário de resultados
        result = {
            "Language": lang.split(" ")[0],
            "Implementation": config["impl"],
            "N": n_val,
            "Time (s)": time_taken,
            "Memory (KB)": mem_usage_kb_total
        }
        
        # Adiciona todos os dados do JSON (solutions, nodes_visited, backtracks, etc.)
        # Isso torna o script robusto para diferentes saídas (Standard vs Bitboard)
        result.update(output_data) 
        
        return result
        
    except subprocess.TimeoutExpired:
        print(f"    Timeout for {lang} at N={n_val}")
        return { "Language": lang.split(" ")[0], "Implementation": config["impl"], "N": n_val, "Time (s)": 300.0, "Solutions": "Timeout" }
    except Exception as e:
        print(f"    Error running {lang} at N={n_val}: {e}")
        if hasattr(e, 'stderr'):
            print(f"    STDERR: {e.stderr.decode()}")
        return None

# --- Main Execution ---
def main():
    if not compile_sources():
        print("Aborting benchmark due to compilation errors.")
        return

    results = []
    
    # Itera sobre os comandos
    for lang, config in COMMANDS.items():
        print(f"\n--- Benchmarking {lang} ---")
        for n in config["n_values"]:
            print(f"    Running N = {n} ({NUM_RUNS} runs)...")
            
            # Novo loop para múltiplas execuções
            for i in range(NUM_RUNS):
                print(f"      Run {i+1}/{NUM_RUNS}...", end='', flush=True)
                result = run_benchmark(lang, config, n)
                
                if result:
                    result['Run'] = i + 1 # Adiciona o número da execução
                    results.append(result)
                    print(f" done. ({result['Time (s)']:.4f}s, {result['Memory (KB)']} KB)")
                else:
                    print(" failed.")
                    # Para o benchmark deste N se uma execução falhar
                    break 

# Write results to CSV
    output_file = "results.csv"
    print(f"\n--- Writing results to {output_file} ---")
    
    if not results:
        print("No results to write.")
        return

    # --- CORREÇÃO: Coletar TODOS os fieldnames ---
    # O problema: Implementações diferentes (Standard vs Bitboard) produzem colunas diferentes.
    # A solução: Fazer um "union" (união) de todas as chaves de todos os dicionários de resultados.
    all_keys = set()
    for res in results:
        all_keys.update(res.keys())
    
    # O cabeçalho agora é COMPLETO.
    fieldnames = list(all_keys)
    
    # Reordena para uma melhor leitura (como antes)
    ordered_fields = ['Language', 'Implementation', 'N', 'Run', 'Time (s)', 'Memory (KB)', 'solutions', 'nodes_visited', 'backtracks', 'pruned_paths', 'explored_placements']
    
    # Filtra apenas os campos que realmente existem no nosso set completo
    final_fieldnames = [f for f in ordered_fields if f in fieldnames]
    
    # Adiciona quaisquer campos extras que não previmos (mas que estavam nos dados)
    for f in fieldnames:
        if f not in final_fieldnames:
            final_fieldnames.append(f)

    try:
        with open(output_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=final_fieldnames)
            writer.writeheader()
            writer.writerows(results)
            
        print("Benchmark complete.")
        print(f"Sucesso! O arquivo '{output_file}' foi criado.")
        print(f"NOTA: A medição de memória (Memory (KB)) usa 'resource.getrusage()', que funciona no Linux/WSL. Os resultados podem ser 0 ou imprecisos no Windows nativo.")
    
    except Exception as e:
        print(f"\n[ERRO FATAL AO ESCREVER O CSV]")
        print(f"  Ocorreu um erro ao salvar o arquivo: {e}")
        print(f"  Fieldnames que o script tentou usar: {final_fieldnames}")


if __name__ == "__main__":
    main()