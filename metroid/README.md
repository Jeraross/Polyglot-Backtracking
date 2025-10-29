# Metroid Analogy Simulator

This directory does **not** solve a classic combinatorial problem. Instead, it provides a practical, visual simulation of the **Backtracking Algorithm** using the *Metroidvania* genre as an analogy.

## The Analogy

* **Samus (Player):** The core backtracking algorithm/function.
* **The Map (World):** The search space (e.g., the decision tree).
* **A Path (Hallway):** A single recursive choice.
* **A Dead End (Red Door):** A violated constraint (e.g., two queens attacking).
* **Backtracking (Returning):** Returning from the recursive call to try a different path (e.g., Samus walking back to the last junction).
* **A Power-Up (Morph Ball):** A new state that "unlocks" previously invalid paths, allowing for re-exploration.

## The Simulation

The programs in this folder read a simple `map.json` file that defines a world layout, connections, and "power-up" requirements for certain paths.

The simulator will then "play" as Samus, attempting to explore the entire map. It will print its logic to the console, showing:
1.  Which path it is attempting.
2.  When it hits a "dead end" (e.g., "Hit Red Door, need Missiles.").
3.  When it "backtracks" to the last junction.
4.  When it finds a "power-up."
5.  How it uses the new power-up to re-explore a previously blocked path.

### `map.json` Structure

The map is defined as a simple graph:

```json
{
  "start_room": "Samus_Ship",
  "rooms": [
    {
      "name": "Samus_Ship",
      "connections": ["Crateria_A"]
    },
    {
      "name": "Crateria_A",
      "connections": ["Samus_Ship", "Crateria_B", "Red_Door_Room"]
    },
    {
      "name": "Crateria_B",
      "connections": ["Crateria_A", "Morph_Ball_Room"]
    },
    {
      "name": "Morph_Ball_Room",
      "item": "Morph_Ball"
    },
    {
      "name": "Red_Door_Room",
      "connections": ["Crateria_A"],
      "requires": "Missiles"
    }
  ]
}
```

## How to Run
All commands should be run from this directory (e.q., Polyglot-Backtracking/metroid/).

### Python
The Python script will automatically look for map.json in the current directory.

```bash
# Run the simulation:
python3 ./python/metroid_sim.py
```

### C++

The C++ version also reads map.json. A Makefile is provided.

```bash

# 1. Compile (using Makefile):
(cd cpp && make)

# 1b. Compile (manually with g++):
# g++ -o ./cpp/metroid_sim ./cpp/metroid_sim.cpp -O2

# 2. Run the simulation:
./cpp/metroid_sim
```