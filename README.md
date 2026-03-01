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
- Tkinter (comes built-in with standard Python installations)

Check Python version:

```bash
python --version
```

Check Tkinter:

```bash
python -m tkinter
```

If a small test window appears, you're good to go.

---

## 📦 Installation

No external packages required.

```bash
# 1. Clone repository
git clone https://github.com/YOUR_USERNAME/dynamic-pathfinder.git

# 2. Navigate into folder
cd dynamic-pathfinder

# 3. Run application
python dynamic_pathfinder.py
```

### Notes

- Windows: use `python` or `py`
- Mac/Linux: use `python3` if needed

---

## 🖥️ How to Use

### Step 1 — Grid Setup

| Action | How |
|--------|-----|
| Set Start | Click **Set Start (S)** → Click a cell |
| Set Target | Click **Set Target (T)** → Click a cell |
| Draw Walls | Click **Draw Wall** → Click or drag |
| Erase Walls | Click **Erase Wall** |
| Generate Random Map | Set Wall % → Click Generate |
| Resize Grid | Set Rows & Cols → Click Apply |

---

### Step 2 — Configure Algorithm

- Choose **Search Strategy**: A* or GBFS  
- Choose **Heuristic Function**: Manhattan, Euclidean, or Chebyshev  

---

### Step 3 — Run

- ▶ **RUN SEARCH**
- ■ **STOP**
- **Clear Path** → clears only path (keeps walls)
- **Reset Grid** → clears everything

---

### Step 4 — Dynamic Mode (Optional)

1. Enable **Dynamic Obstacles**
2. Set **Spawn Probability (%)**
3. Run the search  

The agent will automatically re-plan if its path gets blocked.

---

## 🎨 Colour Guide

| Colour | Meaning |
|--------|----------|
| 🟢 Green | Start Node (S) |
| 🔵 Blue | Target Node (T) |
| 🩷 Pink | Wall / Obstacle |
| 🟡 Yellow | Frontier (Open List) |
| ⬛ Grey | Visited (Closed List) |
| 🟣 Purple | Final Path |
| 🟠 Orange | Moving Agent |

---

## 📁 Project Structure

```
dynamic-pathfinder/
│
├── dynamic_pathfinder.py   # Main application (all code in one file)
└── README.md               # Documentation
```

---

## 🧠 Algorithm Summary

### A* Search

```
f(n) = g(n) + h(n)
```

- g(n) = exact cost from start to node n  
- h(n) = heuristic estimate from node n to goal  
- Optimal and complete when heuristic is admissible  

---

### Greedy Best-First Search

```
f(n) = h(n)
```

- Uses heuristic only  
- Faster than A*  
- Not guaranteed optimal  

---

## 📊 Heuristics Comparison

| Heuristic | Formula | Best For |
|------------|---------|----------|
| Manhattan | \|Δr\| + \|Δc\| | 4-direction grids |
| Euclidean | √(Δr² + Δc²) | Straight-line distance |
| Chebyshev | max(\|Δr\|, \|Δc\|) | 8-direction grids (Recommended) |

---

## ⚠️ Troubleshooting

| Problem | Solution |
|----------|-----------|
| No module named tkinter | Install `python3-tk` (Linux only) |
| Blank window | Ensure Python 3.8+ is being used |
| No path found | Target may be completely surrounded |
| App freezes | Click STOP, try smaller grid or lower wall density |

---

## 📄 License

This project was developed for academic purposes as part of the AI course at FAST NUCES.

---

## ❤️ Author

Made with dedication by  
**Raazia Mehmood (24F-0614)**
