import subprocess
import time
import os
import csv
import json
import resource # Para medir o uso de memória (funciona no Linux/WSL)

# --- Configuration ---
# N=15 é muito lento para os não-bitboard, mas rápido para o bitboard
N_VALUES_STANDARD = range(4, 15) # Para Python, Java, C++ Padrão
N_VALUES_BITBOARD = range(4, 17) # O Bitboard pode ir mais longe

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

# --- Helper Functions ---
def compile_sources():
    """Compile C++ and Java sources."""
    print("--- Compiling all sources ---")
    
    # Compile C++
    try:
        subprocess.run(["make"], cwd=CPP_DIR, check=True, capture_output=True)
        print("C++ compiled successfully.")
    except Exception as e:
        print(f"Error compiling C++: {e}")
        return False

    # Compile Java
    try:
        java_file = os.path.join(JAVA_DIR, "NQueens.java")
        subprocess.run(["javac", java_file], check=True, capture_output=True)
        print("Java compiled successfully.")
    except Exception as e:
        print(f"Error compiling Java: {e}")
        return False
        
    print("--- Compilation complete ---")
    return True

def run_benchmark(lang, config, n_val):
    """Runs a single benchmark and returns results."""
    cmd = [str(n_val) if item == "N" else item for item in config["cmd"]]
    
    try:
        # Reseta o uso de recursos antes de rodar
        resource.setrlimit(resource.RLIMIT_AS, (resource.RLIM_INFINITY, resource.RLIM_INFINITY))
        
        start_time = time.perf_counter()
        
        # Executa o processo
        proc = subprocess.run(
            cmd, 
            check=True, 
            capture_output=True, 
            text=True, 
            timeout=300 # Timeout de 5 minutos para Ns grandes
        )
        
        end_time = time.perf_counter()
        
        # Mede o tempo e o uso de memória
        time_taken = end_time - start_time
        # ru_maxrss é o "Maximum Resident Set Size" em Kilobytes (no Linux)
        mem_usage_kb = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
        
        # Analisa a nova saída JSON
        try:
            output_data = json.loads(proc.stdout.strip())
            solutions = output_data['solutions']
            nodes_visited = output_data['nodes_visited']
        except json.JSONDecodeError:
            print(f"    Error: Could not parse JSON output from {lang}")
            print(f"    STDOUT: {proc.stdout}")
            return None

        return {
            "Language": lang.split(" ")[0],
            "Implementation": config["impl"],
            "N": n_val,
            "Solutions": solutions,
            "NodesVisited": nodes_visited,
            "Time (s)": time_taken,
            "Memory (KB)": mem_usage_kb
        }
        
    except subprocess.TimeoutExpired:
        print(f"    Timeout for {lang} at N={n_val}")
        return {
            "Language": lang.split(" ")[0],
            "Implementation": config["impl"],
            "N": n_val,
            "Solutions": "Timeout",
            "NodesVisited": "Timeout",
            "Time (s)": 300.0,
            "Memory (KB)": 0
        }
    except Exception as e:
        print(f"    Error running {lang} at N={n_val}: {e}")
        print(f"    STDERR: {e.stderr.decode() if hasattr(e, 'stderr') else 'N/A'}")
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
            print(f"    Running N = {n}...")
            result = run_benchmark(lang, config, n)
            if result:
                results.append(result)
                print(f"      ... {result['Time (s)']:.6f}s, {result['Memory (KB)']} KB, {result['NodesVisited']} nodes")

    # Write results to CSV
    output_file = "results.csv"
    print(f"\n--- Writing results to {output_file} ---")
    
    if not results:
        print("No results to write.")
        return

    fieldnames = results[0].keys()
    with open(output_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
        
    print("Benchmark complete.")
    print(f"NOTA: A medição de memória (Memory (KB)) usa 'resource.getrusage()', que funciona no Linux/WSL. Os resultados podem ser 0 ou imprecisos no Windows nativo.")

if __name__ == "__main__":
    main()