import subprocess
import time
import os
import csv

# --- Configuration ---
# Range of N values to test
# Warning: Non-bitboard solutions get very slow after N=14
N_VALUES = range(4, 15) 

# Paths (relative to this script's location)
PROJECT_ROOT = ".."
N_QUEENS_DIR = os.path.join(PROJECT_ROOT, "n-queens")
CPP_DIR = os.path.join(N_QUEENS_DIR, "cpp")
PY_DIR = os.path.join(N_QUEENS_DIR, "python")
JAVA_DIR = os.path.join(N_QUEENS_DIR, "java")

# --- Commands ---
# Note: 'N' will be replaced
COMMANDS = {
    "Python": {
        "cmd": ["python3", os.path.join(PY_DIR, "n_queens.py"), "N"],
        "impl": "Standard"
    },
    "C++ (Standard)": {
        "cmd": [os.path.join(CPP_DIR, "n_queens"), "N"],
        "impl": "Standard"
    },
    "C++ (Bitboard)": {
        "cmd": [os.path.join(CPP_DIR, "n_queens_bitboard"), "N"],
        "impl": "Bitboard"
    },
    "Java": {
        "cmd": ["java", "-cp", JAVA_DIR, "NQueens", "N"],
        "impl": "Standard"
    }
}

# --- Helper Functions ---
def compile_sources():
    """Compile C++ and Java sources."""
    print("--- Compiling all sources ---")
    
    # Compile C++
    try:
        # We run 'make' from within the 'cpp' directory
        subprocess.run(["make"], cwd=CPP_DIR, check=True, capture_output=True)
        print("C++ compiled successfully.")
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"Error compiling C++: {e}")
        if hasattr(e, 'stderr'):
            print(e.stderr.decode())
        return False

    # Compile Java
    try:
        java_file = os.path.join(JAVA_DIR, "NQueens.java")
        subprocess.run(["javac", java_file], check=True, capture_output=True)
        print("Java compiled successfully.")
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"Error compiling Java: {e}")
        if hasattr(e, 'stderr'):
            print(e.stderr.decode())
        return False
        
    print("--- Compilation complete ---")
    return True

def run_benchmark(lang, config, n_val):
    """Runs a single benchmark and returns results."""
    # Replace 'N' placeholder with the actual value
    cmd = [str(n_val) if item == "N" else item for item in config["cmd"]]
    
    try:
        start_time = time.perf_counter()
        proc = subprocess.run(
            cmd, 
            check=True, 
            capture_output=True, 
            text=True, 
            timeout=60 # 60-second timeout
        )
        end_time = time.perf_counter()
        
        time_taken = end_time - start_time
        solutions = int(proc.stdout.strip())
        
        return {
            "Language": lang.split(" ")[0], # "C++ (Standard)" -> "C++"
            "Implementation": config["impl"],
            "N": n_val,
            "Solutions": solutions,
            "Time (s)": time_taken
        }
        
    except subprocess.TimeoutExpired:
        print(f"    Timeout for {lang} at N={n_val}")
        return {
            "Language": lang.split(" ")[0],
            "Implementation": config["impl"],
            "N": n_val,
            "Solutions": "Timeout",
            "Time (s)": 60.0
        }
    except Exception as e:
        print(f"    Error running {lang} at N={n_val}: {e}")
        return None

# --- Main Execution ---
def main():
    if not compile_sources():
        print("Aborting benchmark due to compilation errors.")
        return

    results = []
    
    for n in N_VALUES:
        print(f"\n--- Benchmarking N = {n} ---")
        for lang, config in COMMANDS.items():
            # The bitboard solution is so fast, the standard one is redundant
            # Let's skip the standard C++ if N is large (e.g., > 13)
            if lang == "C++ (Standard)" and n > 13:
                print("    Skipping C++ (Standard) for large N.")
                continue

            print(f"    Running {lang}...")
            result = run_benchmark(lang, config, n)
            if result:
                results.append(result)
                print(f"      ... {result['Solutions']} solutions in {result['Time (s)']:.6f}s")

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

if __name__ == "__main__":
    main()