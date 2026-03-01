# Dynamic-Pathfinding-Agent-Informed-Search-A-GBFS
An interactive grid-based pathfinding visualiser implementing A* and Greedy Best-First Search (GBFS) with dynamic obstacle re-planning. Built with Python &amp; Tkinter — no external libraries required. 
*Student: Raazia Mehmood | Roll No: 24F-0614 University: NUCES, Chiniot-Faisalabad Campus*

📸 Preview
A* Search	Greedy Best-First
Explores optimally using f(n) = g(n) + h(n)	Fast greedy search using f(n) = h(n)
✨ Features
✅ A* Search — optimal, complete, uses combined cost + heuristic
✅ Greedy Best-First Search (GBFS) — fast, heuristic-only search
✅ 3 Heuristics — Manhattan, Euclidean, Chebyshev (switchable from GUI)
✅ 8-Directional Movement — cardinal + diagonal (diagonal cost = √2)
✅ Dynamic Obstacles — walls spawn mid-search; agent re-plans in real time
✅ Interactive Map Editor — draw/erase walls, set start & target by clicking
✅ Random Map Generator — user-defined wall density (%)
✅ Custom Grid Size — from 5×5 up to 30×30
✅ Live Metrics Dashboard — nodes visited, path cost, execution time (ms), re-plan count
✅ Color-coded Visualisation — frontier (yellow), visited (grey), path (purple), agent (orange)
🚀 Getting Started
Prerequisites
Python 3.8 or higher
Tkinter (comes built-in with standard Python installations)
Check Python version
python --version
Check Tkinter is available
python -m tkinter
A small test window should appear. If it does, you're good to go.

📦 Installation
No external packages needed. Just clone and run.

# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/dynamic-pathfinder.git

# 2. Navigate into the project folder
cd dynamic-pathfinder

# 3. Run the application
python dynamic_pathfinder.py
Windows users: Use python or py
Mac/Linux users: Use python3 if python points to Python 2

🖥️ How to Use
Step 1 — Set Up the Grid
Action	How
Set Start node	Click "Set Start (S)" → click a cell
Set Target node	Click "Set Target (T)" → click a cell
Draw walls	Click "Draw Wall" → click or drag on grid
Erase walls	Click "Erase Wall" → click on a wall cell
Generate random map	Set Wall % → click "Generate Random Map"
Resize grid	Set Rows & Cols → click "Apply Grid Size"
Step 2 — Configure the Algorithm
Choose Search Strategy: A* or Greedy Best-First (GBFS)
Choose Heuristic Function: Manhattan, Euclidean, or Chebyshev
Step 3 — Run
Click ▶ RUN SEARCH to start
Click ■ STOP to interrupt at any time
Click Clear Path to reset visualisation (keeps walls)
Click Reset Grid to start completely fresh
Step 4 — Dynamic Mode (Optional)
Tick "Enable Dynamic Obstacles"
Set Spawn prob (%) — chance of a new wall appearing at each agent step
Run the search — the agent will automatically re-plan if its path gets blocked
🎨 Colour Guide
Colour	Meaning
🟢 Green	Start node (S)
🔵 Blue	Target node (T)
🩷 Pink	Wall / obstacle
🟡 Yellow	Frontier (open list)
⬛ Dark grey	Visited (closed list)
🟣 Purple	Final path
🟠 Orange	Moving agent
📁 Project Structure
dynamic-pathfinder/
│
├── dynamic_pathfinder.py   # Main application — all code in one file
└── README.md               # This file
🧠 Algorithm Summary
A* Search
f(n) = g(n) + h(n)
g(n) = exact cost from start to node n
h(n) = heuristic estimate from n to goal
Optimal and complete when heuristic is admissible
Greedy Best-First Search
f(n) = h(n)
Ignores path cost, only follows heuristic
Faster than A* but not optimal or complete
Heuristics
Name	Formula	Best For
Manhattan	|Δr| + |Δc|	4-directional grids
Euclidean	√(Δr² + Δc²)	Straight-line distance
Chebyshev	max(|Δr|, |Δc|)	8-directional grids ✅ recommended
⚠️ Troubleshooting
Problem	Fix
No module named tkinter	Run sudo apt-get install python3-tk (Linux only)
Window appears but is blank	Ensure Python 3.8+ is being used
Search finds no path	The target may be completely surrounded — erase some walls
App freezes during search	Click ■ STOP, then try a smaller grid or lower wall density
📄 License
This project was developed for academic purposes as part of the AI course at NUCES FAST.

Made with ❤️ by Raazia Mehmood 24F-0614

