# N-Queens Genetic Algorithm Solver

This project implements a **Genetic Algorithm (GA)** to solve the classic N-Queens problem — placing N chess queens on an N×N board such that no two queens attack each other. The algorithm evolves a population of candidate solutions across multiple generations using selection, crossover, and mutation operators, tracking fitness improvements over time and visualizing the results through both a smoothed graph and an interactive Tkinter chessboard GUI.

## How It Works

Each individual in the population is represented as a list of N integers, where the value at index `i` denotes the row position of the queen in column `i`. Fitness is calculated by counting the number of non-attacking queen pairs — the maximum possible fitness for N queens is `N*(N-1)/2`. At each generation, individuals are selected proportionally to their fitness (roulette wheel selection), paired up for single-point crossover at a randomly chosen split index, and then mutated by swapping two randomly chosen positions within each individual. The algorithm tracks both the average fitness and the best fitness per generation, saving the globally best configuration encountered across all iterations. After all generations complete, a smoothed fitness graph is saved as `fitness_plot.png` and a Tkinter window opens displaying the best queen arrangement on a styled chessboard.

## Changing N-Queens and Iterations

To experiment with different board sizes and run lengths, modify these three variables at the bottom of the script:

```python
p_size    = 10     # Number of individuals in the population
N_queens  = 8      # Board size — change this to 4, 16, 32, 50, etc.
iterations = 500   # Number of generations to run
```

For smaller boards like `N_queens = 4`, the algorithm converges very quickly — reducing `iterations` to `50` is enough to see the curve plateau. For larger boards like `N_queens = 32` or `N_queens = 50`, increasing `iterations` to `1000+` and `p_size` to `20` gives the algorithm enough room to meaningfully improve. The fitness graph will automatically rescale its Y-axis ticks to match the value range, so the visualization stays readable at any board size.

## Installation

This project requires Python 3 and the following libraries. Install them using the exact names below:

```bash
# Core scientific and plotting libraries
pip install numpy
pip install matplotlib
pip install scipy

# Tkinter (GUI — install via system package manager, not pip)

# Arch Linux
sudo pacman -S tk

# Ubuntu / Debian
sudo apt install python3-tk tk-dev -y
```

To verify Tkinter is working correctly before running the script:

```bash
python -c "import tkinter; tkinter._test()"
```

A small test window should appear. Once all dependencies are installed, run the solver with:

```bash
python 24L-0717_asg2.py
```

The script will print per-generation fitness stats to the terminal, save `fitness_plot.png` in the current directory, and open the chessboard GUI showing the best solution found.
