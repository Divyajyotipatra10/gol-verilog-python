# Conway’s Game of Life — Hardware Simulation with Verilog & Python
This project implements Conway’s Game of Life (GOL) using Verilog for simulation logic and Python for GUI interaction and visualization. The game logic, including toroidal boundary handling, is entirely written in Verilog and simulated using ModelSim. Input patterns are passed from a custom Tkinter-based GUI, and the output of the simulation is visualized using Pygame as a dynamic 16×16 grid.

## Project Overview
1. Game logic and testbench in Verilog
2. Simulated using ModelSim via .tcl automation
3. Inputs selected or custom-designed using a Python GUI
4. Simulation results visualized in real-time using Pygame

## Project Motivation
Most Game of Life implementations are software-based — written in Python, Java, or JavaScript. This project explores how hardware-level logic using Verilog can simulate the same system efficiently, and how such logic can be controlled and visualized through a hybrid Python interface.
1. It serves as a bridge between:
2. Hardware Description Languages (HDLs) like Verilog for algorithm simulation
3. Scripting tools like Python for GUI and user interaction
4. Waveform-based simulation tools like ModelSim for backend logic

## Game Rules & Grid Topology
Conway’s Game of Life evolves based on these standard rules applied at each clock cycle:

| Number of Live Neighbors | Next State of Cell |
|--------------------------|---------------------|
| 0 or 1                   | Dead (`0`)          |
| 2                        | No Change           |
| 3                        | Alive (`1`)         |
| 4 or more                | Dead (`0`)          |

## Toroidal Grid
The game is played on a 16×16 toroidal grid — meaning edges wrap around like a donut.
For example, the corner cell (0,0) has 8 neighbors:
(15,15), (15,0), (15,1),
(0,15),  (0,0),   (0,1),
(1,15),  (1,0),  (1,1)
This wrap-around behavior is handled entirely in the Verilog logic.

##  Bit Vector Representation
The grid is stored as a flattened 256-bit vector q[255:0]
Row-wise packing is done as:
q[0:15] → Row 0
q[16:31] → Row 1
…
q[240:255] → Row 15

## Simulation Setup
Simulated the Game of Life using ModelSim with a TCL do file:
The Verilog testbench loads an initial grid state through a file (user_input.txt)
The simulation updates the grid every clock cycle
Final results are written into sim_output.txt

Simulation is invoked as:
vsim -c -do "do tb_do_file.tcl"

![image](https://github.com/user-attachments/assets/3515ba13-cf1b-473a-8dd7-1eb87a54014c)
![image](https://github.com/user-attachments/assets/518c3d7e-2628-4cd4-8853-bab5d92ea830) 
![image](https://github.com/user-attachments/assets/55d96bea-05cb-4b42-93eb-cc95dd13d9a3)

## Python GUI
A Python GUI (built using Tkinter) allows you to:
Select predefined patterns (e.g., Still Life, Oscillator, Spaceship)
Design a custom pattern by clicking on a 16×16 grid
Send the pattern to Verilog by writing a 256-bit hex string to the input file
Start the simulation and launch visualization from the same interface

## GUI Screenshot
![image](https://github.com/user-attachments/assets/31241b68-fdaf-4d2e-b447-af0dd7fbdeac)  ![image](https://github.com/user-attachments/assets/e00fcbae-7880-4867-b371-4af9551d5f45)
![image](https://github.com/user-attachments/assets/e4f1a2b7-80a6-465c-85ce-2ba88339fdd8)
![image](https://github.com/user-attachments/assets/6bfb396b-ec9f-4f61-904c-9a815bb88dd4)  ![image](https://github.com/user-attachments/assets/6ba5f877-acad-4128-8ffc-e3fb8a4fed48)

##  Pygame Visualization
Once simulation is complete (or during execution), the output is continuously read and rendered using Pygame:
Live 16×16 grid visualization
White squares = alive cells
Dark squares = dead cells
Auto-refreshes every few milliseconds with new frames
## Pygame Visualization Example
![image](https://github.com/user-attachments/assets/ad19d86d-06c4-48cc-a482-8ca8043f3108)  ![image](https://github.com/user-attachments/assets/1b4df2f8-0758-4154-90e6-db4c0b479554)

## License
This project is open-source under the MIT License — you are free to use, modify, and distribute with attribution.















