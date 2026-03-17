import random
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline
import tkinter as tk

graph_y_avg = list()
graph_y_max = list()
graph_x = list()

best_fitness_ever = 0
best_config_ever = []


def plotgraph():
    xpoints = np.array(graph_x)
    avg_points = np.array(graph_y_avg)
    max_points = np.array(graph_y_max)

    window = 10
    avg_smoothed = np.convolve(avg_points, np.ones(window)/window, mode='valid')
    max_smoothed = np.convolve(max_points, np.ones(window)/window, mode='valid')
    x_smoothed = xpoints[:len(avg_smoothed)]

    def make_spline(x, y):
        if len(x) >= 4:
            x_interp = np.linspace(x.min(), x.max(), 300)
            spline = make_interp_spline(x, y, k=3)
            return x_interp, spline(x_interp)
        return x, y

    x_avg, y_avg = make_spline(x_smoothed, avg_smoothed)
    x_max, y_max = make_spline(x_smoothed, max_smoothed)

    all_vals = np.concatenate([y_avg, y_max])
    y_min = float(np.min(all_vals))
    y_max_val = float(np.max(all_vals))
    raw_step = (y_max_val - y_min) / 10
    magnitude = 10 ** int(np.floor(np.log10(raw_step))) if raw_step > 0 else 1
    step = max(1, round(raw_step / magnitude) * magnitude)

    plt.figure(figsize=(12, 6))
    plt.plot(x_avg, y_avg, color='royalblue', linewidth=2, label='Avg Fitness')
    plt.plot(x_max, y_max, color='crimson', linewidth=2, linestyle='--', label='Max Fitness')

    plt.xlabel("GENERATIONS")
    plt.ylabel("FITNESS")
    plt.title("Genetic Algorithm - Fitness over Generations")
    plt.yticks(np.arange(y_min, y_max_val + step, step))
    plt.xticks(xpoints[::max(1, len(xpoints)//20)])
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig("fitness_plot.png")
    print("Plot saved as fitness_plot.png")


def show_gui(config, fitness, N_queens):
    root = tk.Tk()
    root.title(f"Best N-Queens Configuration | Fitness: {fitness}")
    root.configure(bg="#1a1a2e")

    # ── Header ──────────────────────────────────────────────
    header = tk.Frame(root, bg="#1a1a2e")
    header.pack(pady=(18, 4))

    tk.Label(
        header,
        text="♛  N-Queens Best Solution",
        font=("Georgia", 20, "bold"),
        fg="#e0c97f",
        bg="#1a1a2e"
    ).pack()

    tk.Label(
        header,
        text=f"N = {N_queens}   |   Best Fitness = {fitness}   |   Max Possible = {N_queens*(N_queens-1)//2}",
        font=("Courier New", 11),
        fg="#a0aec0",
        bg="#1a1a2e"
    ).pack(pady=(4, 0))

    # ── Board ────────────────────────────────────────────────
    board_frame = tk.Frame(root, bg="#1a1a2e", padx=16, pady=12)
    board_frame.pack()

    cell = max(10, min(54, 480 // N_queens))   # responsive cell size

    canvas = tk.Canvas(
        board_frame,
        width=cell * N_queens,
        height=cell * N_queens,
        highlightthickness=2,
        highlightbackground="#e0c97f",
        bg="#1a1a2e"
    )
    canvas.pack()

    for row in range(N_queens):
        for col in range(N_queens):
            color = "#f0d9b5" if (row + col) % 2 == 0 else "#b58863"
            canvas.create_rectangle(
                col * cell, row * cell,
                (col + 1) * cell, (row + 1) * cell,
                fill=color, outline=""
            )

    for col, row in enumerate(config):
        r = row - 1          # convert 1-indexed → 0-indexed
        cx = col * cell + cell // 2
        cy = r  * cell + cell // 2
        font_size = max(8, int(cell * 0.55))
        canvas.create_text(
            cx, cy,
            text="♛",
            font=("Arial", font_size),
            fill="#1a1a0a"
        )

    cfg_str = "  ".join(str(v) for v in config)
    tk.Label(
        root,
        text=f"Column positions:  [ {cfg_str} ]",
        font=("Courier New", 9),
        fg="#718096",
        bg="#1a1a2e",
        wraplength=cell * N_queens + 32
    ).pack(pady=(0, 16))

    root.mainloop()


def Selection(sample, t_fitness, fitness, p_size, new_population):
    if t_fitness == 0:
        return
    probability = fitness / t_fitness
    actual_prob = round(probability * p_size)
    for i in range(actual_prob):
        new_population.append([0, sample[:]])


def calculate_fitness(sample, N_queens):
    fitness = 0
    for i in range(N_queens):
        for j in range(i + 1, N_queens):
            if (sample[i] != sample[j] and
                    abs(i - j) != abs(sample[i] - sample[j])):
                fitness += 1
    return fitness


def print_population(population, p_size):
    print("------PRINTING POPULATION------")
    for i in range(p_size):
        print(population[i][1])


def mutation(population, i, N_queens):
    if i + 1 >= len(population):
        return
    idx1, idx2 = random.sample(range(N_queens), 2)
    population[i][1][idx1], population[i][1][idx2] = (
        population[i][1][idx2], population[i][1][idx1]
    )
    idx1, idx2 = random.sample(range(N_queens), 2)
    population[i + 1][1][idx1], population[i + 1][1][idx2] = (
        population[i + 1][1][idx2], population[i + 1][1][idx1]
    )


def cross_over(population, p_size, N_queens):
    actual_size = len(population)
    if actual_size % 2 != 0:
        actual_size -= 1
    for i in range(0, actual_size, 2):
        cross_over_point = random.randint(1, N_queens - 2)
        for j in range(cross_over_point, N_queens):
            population[i][1][j], population[i + 1][1][j] = (
                population[i + 1][1][j], population[i][1][j]
            )
        mutation(population, i, N_queens)


def Genetic_Algo(population, p_size, N_queens):
    global best_fitness_ever, best_config_ever

    t_fitness = 0
    fittest = 0
    best_config_this_gen = []
    new_population = list()

    for i in range(p_size):
        fitness = calculate_fitness(population[i][1], N_queens)
        population[i][0] = fitness
        t_fitness += fitness
        if fitness > fittest:
            fittest = fitness
            best_config_this_gen = population[i][1][:]
        print("Fitness of individual ", i + 1, ": ", fitness)

    avg = t_fitness // p_size
    print("Average Fitness: ", avg)
    print("Best Fitness: ", fittest)

    graph_y_avg.append(avg)
    graph_y_max.append(fittest)

    if fittest > best_fitness_ever:
        best_fitness_ever = fittest
        best_config_ever = best_config_this_gen
        print(f"  ★ New global best: {best_fitness_ever}")

    for i in range(p_size):
        Selection(population[i][1], t_fitness, population[i][0],
                  p_size, new_population)

    if not new_population:
        print("Warning: selection produced empty population, skipping generation.")
        return

    population[:] = new_population
    cross_over(population, len(population), N_queens)


def Genetic_algo_itr(population, p_size, N_queens):
    iterations = 500
    print_population(population, p_size)
    for i in range(iterations):
        print("------Iteration #", i + 1, " ------")
        Genetic_Algo(population, len(population), N_queens)
        graph_x.append(i + 1)


def Initialization(p_size, N_queens):
    population = list()
    for i in range(p_size):
        sample = [random.randint(1, N_queens) for _ in range(N_queens)]
        population.append([0, sample])
    return population


p_size = 10
N_queens = 20
population = Initialization(p_size, N_queens)
Genetic_algo_itr(population, p_size, N_queens)

print(f"\n★ Overall Best Fitness: {best_fitness_ever}")
print(f"★ Best Configuration:  {best_config_ever}")

plotgraph()
show_gui(best_config_ever, best_fitness_ever, N_queens)