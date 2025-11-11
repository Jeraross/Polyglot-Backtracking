## How to Run

First, compile the C++ and Java code:

```bash
# Compile C++ (from the root directory)
make -C n-queens/cpp

# Compile Java
javac n-queens/java/NQueens.java
````

This is the main workflow of the project, split into two parts: **generating** the data and **visualizing** it.

#### Part A: Generate the Benchmark Data

1.  Navigate to the `analysis` directory:

    ```bash
    cd analysis
    ```

2.  Run the benchmark script:

    ```bash
    python3 benchmark_all.py
    ```

    This script will automatically compile all sources and run them for a wide range of `N` values. It may take several minutes to complete. When finished, it will create (or overwrite) `analysis/results.csv` with the new data.

#### Part B: View the Analysis in Jupyter

1.  Ensure you are still in the `analysis` directory.

2.  Start the Jupyter Lab server:

    ```bash
    jupyter lab
    ```

3.  Your terminal will output several links. Copy one of the links (e.g., `http://localhost:8888/lab?token=...`) and paste it into your web browser.

4.  The Jupyter interface will open. From the file list on the left, click on `charts.ipynb`.

5.  With the notebook open, go to the menu bar at the top and click:
    **`Run`** → **`Run All Cells`**

6.  Scroll down through the notebook to see all the generated plots and the detailed, multi-axis analysis of the results.