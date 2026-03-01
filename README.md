# Dynamic Pathfinding Agent — Informed Search (A* & GBFS)

An interactive grid-based pathfinding visualiser implementing **A*** and **Greedy Best-First Search (GBFS)** with dynamic obstacle re-planning.

Built using **Python** and **Tkinter** (no external libraries required).

---

## 👩‍🎓 Student Information

**Name:** Raazia Mehmood  
**Roll No:** 24F-0614  
**University:** NUCES (FAST), Chiniot-Faisalabad Campus  

---

## 📸 Preview

| A* Search | Greedy Best-First Search |
|------------|--------------------------|
| Explores optimally using `f(n) = g(n) + h(n)` | Fast greedy search using `f(n) = h(n)` |

---

## ✨ Features

- ✅ **A* Search** — Optimal and complete (cost + heuristic)
- ✅ **Greedy Best-First Search (GBFS)** — Fast heuristic-based search
- ✅ **3 Heuristics** — Manhattan, Euclidean, Chebyshev
- ✅ **8-Directional Movement** — Cardinal + Diagonal (Diagonal cost = √2)
- ✅ **Dynamic Obstacles** — Agent re-plans automatically if blocked
- ✅ **Interactive Map Editor**
- ✅ **Random Map Generator**
- ✅ **Custom Grid Size (5×5 → 30×30)**
- ✅ **Live Metrics Dashboard**
- ✅ **Color-coded Visualisation**

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Tkinter (comes built-in with standard Python)

Check Python version:
python --version
Check Tkinter:
python -m tkinter
python -m tkinter

If a small window appears → you're good to go.

📦 Installation

No external packages required.

# 1. Clone repository
git clone https://github.com/YOUR_USERNAME/dynamic-pathfinder.git

# 2. Navigate into folder
cd dynamic-pathfinder

# 3. Run application
python dynamic_pathfinder.py
Notes:

Windows: use python or py

Mac/Linux: use python3 if needed

🖥️ How to Use
Step 1 — Grid Setup
Action	How
Set Start	Click Set Start (S) → Click cell
Set Target	Click Set Target (T) → Click cell
Draw Walls	Click Draw Wall → Click/Drag
Erase Walls	Click Erase Wall
Random Map	Set Wall % → Click Generate
Resize Grid	Set Rows & Cols → Apply
Step 2 — Configure Algorithm

Select Search Strategy: A* or GBFS

Select Heuristic: Manhattan, Euclidean, Chebyshev

Step 3 — Run

▶ RUN SEARCH

■ STOP

Clear Path → clears only path

Reset Grid → clears everything

Step 4 — Dynamic Mode (Optional)

Enable Dynamic Obstacles

Set Spawn Probability (%)

Run search
Agent will automatically re-plan if blocked.

🎨 Colour Guide
Colour	Meaning
🟢 Green	Start Node
🔵 Blue	Target Node
🩷 Pink	Wall
🟡 Yellow	Frontier
⬛ Grey	Visited
🟣 Purple	Final Path
🟠 Orange	Agent
📁 Project Structure
dynamic-pathfinder/
│
├── dynamic_pathfinder.py   # Main application
└── README.md               # Documentation
🧠 Algorithm Summary
A* Search
f(n) = g(n) + h(n)

g(n) = cost from start

h(n) = heuristic estimate to goal

Optimal and complete (with admissible heuristic)

Greedy Best-First Search
f(n) = h(n)

Ignores path cost

Faster but not optimal

📊 Heuristics Comparison
Heuristic	Formula	Best For
Manhattan		Δr
Euclidean	√(Δr² + Δc²)	Straight-line
Chebyshev	max(	Δr
⚠️ Troubleshooting
Problem	Solution
No module named tkinter	Install python3-tk (Linux)
Blank window	Ensure Python 3.8+
No path found	Target may be surrounded
App freezes	Stop & reduce grid size
📄 License

Developed for academic purposes (AI Course – FAST NUCES).

❤️ Author

Made with dedication by
Raazia Mehmood (24F-0614)
