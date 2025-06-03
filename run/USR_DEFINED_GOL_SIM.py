import tkinter as tk
from tkinter import messagebox
import subprocess
import threading
import os
import pygame
import time

# --- Configurations ---
do_file = "tb_do_file.tcl"  # TCL file to run ModelSim simulation
working_dir = r"F:/conway_gol/run"  # Working directory containing input/output files # change working directory as per your need
input_file = os.path.join(working_dir, "user_input.txt")  # File to write input pattern
output_file = os.path.join(working_dir, "sim_output.txt")  # Simulation output (binary)
vsim_cmd = ["vsim", "-c", "-do", f"do {do_file}"]  # Command to run ModelSim in console mode

CELL_SIZE = 30  # Size of each cell in grid
GRID_WIDTH = 16  # Width of the simulation grid
GRID_HEIGHT = 16  # Height of the simulation grid
UPDATE_INTERVAL = 200  # Time between frames in milliseconds

# Predefined binary patterns for simulation (hex-encoded)
pattern_data = {
    "Still Life":   "000000000000000000660000006600000006C000000C60000000000000000000",
    "Oscillator":   "0000000000000000007000000038700000700000000000000F0F000000000000",
    "Spaceship":    "000000000000800000400000E00000000000000000000000F800100080010000",
    "Methuselah":   "0000000000000000000000000000000000000000000000100061800410007800",
    "Random":       "A5A549124A8A58B3B49D084C12F03A14CA5D29C183EE0149381A432140AC5A29",
    "Custom":       ""
}

# --- GUI Application Class ---
class GameOfLifeGUI:
    def __init__(self, root):
        # Initialize main window
        self.root = root
        self.root.title("Game of Life Simulator")
        self.root.geometry("600x400")

        # Selected pattern (string variable bound to radio buttons)
        self.selected_pattern = tk.StringVar()
        self.selected_pattern.set(None)

        # Pattern selection radio buttons
        tk.Label(root, text="Select Initial Pattern:", font=("Arial", 14)).pack(pady=10)
        for pattern in pattern_data.keys():
            tk.Radiobutton(root, text=pattern, variable=self.selected_pattern,
                           value=pattern, font=("Arial", 11)).pack(anchor='w', padx=40)

        # Buttons for input, simulation, and visualization
        self.input_button = tk.Button(root, text="Provide Input", font=("Arial", 12),
                                      command=self.provide_input)
        self.input_button.pack(pady=10)

        self.sim_button = tk.Button(root, text="Start Simulation", font=("Arial", 12),
                                    command=self.run_simulation, state="disabled")
        self.sim_button.pack(pady=10)

        self.status_label = tk.Label(root, text="Status: Waiting for input", fg="blue", font=("Arial", 11))
        self.status_label.pack(pady=5)

        self.play_button = tk.Button(root, text="Play Visualization", font=("Arial", 12),
                                     command=self.play_visualization, state="disabled")
        self.play_button.pack(pady=10)

    # Handles pattern input
    def provide_input(self):
        pattern = self.selected_pattern.get()
        if not pattern:
            messagebox.showwarning("Warning", "Please select a pattern.")
            return

        # Launch custom editor if "Custom" is selected
        if pattern == "Custom":
            self.open_custom_pattern_editor()
            return

        # Write pattern to input file
        with open(input_file, "w") as f:
            f.write(pattern_data[pattern])

        self.status_label.config(text="Input written. Ready to simulate.", fg="orange")
        self.sim_button.config(state="normal")

    # GUI for drawing custom pattern
    def open_custom_pattern_editor(self):
        def save_custom_pattern():
            # Convert drawn grid to binary string and write to file
            bits = ''.join(['1' if cell_states[y][x] else '0'
                            for y in range(GRID_HEIGHT) for x in range(GRID_WIDTH)])
            hex_data = f"{int(bits, 2):064X}"  # Convert binary to 64-digit hex
            with open(input_file, 'w') as f:
                f.write(hex_data)
            top.destroy()
            self.status_label.config(text="Custom input written. Ready to simulate.", fg="orange")
            self.sim_button.config(state="normal")

        # Draw GUI window for grid editor
        top = tk.Toplevel(self.root)
        top.title("Custom Pattern Editor")
        canvas = tk.Canvas(top, width=CELL_SIZE * GRID_WIDTH, height=CELL_SIZE * GRID_HEIGHT)
        canvas.pack()

        # Initialize grid with False (off)
        cell_states = [[False for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

        def toggle_cell(event):
            x, y = event.x // CELL_SIZE, event.y // CELL_SIZE
            if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
                cell_states[y][x] = not cell_states[y][x]
                draw_cells()

        def draw_cells():
            canvas.delete("all")
            for y in range(GRID_HEIGHT):
                for x in range(GRID_WIDTH):
                    color = "white" if cell_states[y][x] else "black"
                    canvas.create_rectangle(
                        x * CELL_SIZE, y * CELL_SIZE,
                        (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE,
                        fill=color, outline="gray")

        canvas.bind("<Button-1>", toggle_cell)
        draw_cells()
        tk.Button(top, text="OK", font=("Arial", 12), command=save_custom_pattern).pack(pady=10)

    # Run ModelSim simulation
    def run_simulation(self):
        self.status_label.config(text="Simulation running... A maximum of simulation upto 10 seconds", fg="orange")
        self.sim_button.config(state="disabled")
        self.play_button.config(state="normal")  # Allow immediate playback if desired
        threading.Thread(target=self._run_vsim, daemon=True).start()  # Run simulation in background

    def _run_vsim(self):
        try:
            subprocess.run(vsim_cmd, cwd=working_dir, check=True)  # Run vsim command
            self.status_label.config(text="Simulation complete.", fg="green")
        except subprocess.CalledProcessError:
            self.status_label.config(text="Simulation failed.", fg="red")
        except FileNotFoundError:
            self.status_label.config(text="'vsim' not found.", fg="red")
            messagebox.showerror("Error", "vsim not found. Check ModelSim installation.")
        finally:
            self.sim_button.config(state="normal")

    # Run pygame-based visualizer
    def play_visualization(self):
        if not os.path.exists(output_file):
            messagebox.showerror("Error", f"{output_file} not found.")
            return
        self.root.destroy()
        run_pygame_visualization(output_file)

# --- Pygame Grid Viewer ---
def run_pygame_visualization(output_file):
    pygame.init()
    screen = pygame.display.set_mode((CELL_SIZE * GRID_WIDTH, CELL_SIZE * GRID_HEIGHT))
    pygame.display.set_caption("Game of Life Simulation - 16x16 Grid")
    clock = pygame.time.Clock()

    lines = []  # Holds lines from simulation output
    idx = 0     # Current line index
    running = True

    UPDATE_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(UPDATE_EVENT, UPDATE_INTERVAL)  # Timer for updating frame

    def load_new_lines():
        nonlocal lines
        try:
            with open(output_file, 'r') as f:
                new_lines = [line.strip() for line in f if line.strip()]
            if len(new_lines) > len(lines):  # Only update if new lines were added
                lines = new_lines
        except Exception:
            pass

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == UPDATE_EVENT:
                load_new_lines()
                if idx < len(lines):
                    binary_str = lines[idx].zfill(GRID_WIDTH * GRID_HEIGHT)[:GRID_WIDTH * GRID_HEIGHT]
                    draw_grid(screen, binary_str)
                    idx += 1
                elif idx > 0 and len(lines) > 0:
                    draw_grid(screen, lines[-1].zfill(GRID_WIDTH * GRID_HEIGHT))  # Hold last state

        clock.tick(60)

    pygame.quit()

# Draw grid of white/black squares based on binary string
def draw_grid(screen, bits):
    screen.fill((0, 0, 0))  # Clear screen
    for i, bit in enumerate(bits):
        x = (i % GRID_WIDTH) * CELL_SIZE
        y = (i // GRID_WIDTH) * CELL_SIZE
        color = (255, 255, 255) if bit == '1' else (30, 30, 30)
        rect = pygame.Rect(x, y, CELL_SIZE - 1, CELL_SIZE - 1)
        pygame.draw.rect(screen, color, rect)
    pygame.display.flip()

# --- Start GUI ---
if __name__ == "__main__":
    root = tk.Tk()
    app = GameOfLifeGUI(root)
    root.mainloop()
