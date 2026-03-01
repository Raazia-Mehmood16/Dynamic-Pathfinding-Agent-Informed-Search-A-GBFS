
import tkinter as tk
from tkinter import ttk, messagebox
import heapq
import random
import time

# ─────────────────────────────────────────────
#  GLOBAL CONFIGURATION
# ─────────────────────────────────────────────
DEFAULT_ROWS    = 15
DEFAULT_COLS    = 15
CELL_SIZE       = 40
ANIMATION_DELAY = 0.03   # seconds between steps

# Colors
C_EMPTY    = "#041a3c"   # deep navy background
C_GRID     = "#900649"   # soft grid lines
C_OBSTACLE = "#ff4c4c"   # bright red walls
C_START    = "#00ff9f"   # neon green
C_TARGET   = "#00bfff"   # cyan blue
C_VISITED  = "#1f4068"   # explored nodes
C_FRONTIER = "#ffd166"   # golden yellow
C_PATH     = "#00f5d4"   # bright aqua path
C_AGENT    = "#c0025b"   # orange agent
C_TEXT_DIM = "#5c6f91"
C_TEXT     = "#e6f1ff"

# Movement directions (8-directional)
MOVES = [
    (-1, 0),  (1, 0),   (0, -1),  (0, 1),   # 4-directional cardinal
    (-1,-1),  (-1, 1),  (1, -1),  (1,  1),  # diagonal
]
DIAGONAL_MOVES = {(-1,-1),(-1,1),(1,-1),(1,1)}


# ─────────────────────────────────────────────
#  NODE CLASS
# ─────────────────────────────────────────────
class Node:
    """Represents one cell in the grid during search."""
    def __init__(self, r, c, parent=None, g=0, h=0):
        self.r = r
        self.c = c
        self.parent = parent
        self.g = g      # cost from start
        self.h = h      # heuristic estimate to goal
        self.f = g + h  # total cost (used by A*)

    def pos(self):
        return (self.r, self.c)

    # Comparison for heapq (priority queue)
    def __lt__(self, other):
        return self.f < other.f

    def __eq__(self, other):
        return self.pos() == other.pos()


# ─────────────────────────────────────────────
#  HEURISTIC FUNCTIONS
# ─────────────────────────────────────────────
def heuristic_manhattan(r, c, gr, gc):
    return abs(r - gr) + abs(c - gc)

def heuristic_euclidean(r, c, gr, gc):
    return ((r - gr) ** 2 + (c - gc) ** 2) ** 0.5

def heuristic_chebyshev(r, c, gr, gc):
    """Good for 8-directional movement."""
    return max(abs(r - gr), abs(c - gc))


# ─────────────────────────────────────────────
#  MAIN APPLICATION
# ─────────────────────────────────────────────
class DynamicPathfinderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dynamic Pathfinding Agent — Informed Search")
        self.root.configure(bg="#061425")

        self.rows = DEFAULT_ROWS
        self.cols = DEFAULT_COLS

        # State
        self.grid          = []      # 0 = empty, -1 = wall
        self.rects         = {}      # canvas rectangle IDs
        self.start_pos     = None
        self.target_pos    = None
        self.mode          = "Wall"
        self.running       = False
        self.dynamic_mode  = False
        self.current_path  = []      # current planned path (list of (r,c))
        self.agent_pos     = None    # agent's current position during animation

        # Metrics
        self.nodes_visited = 0
        self.path_cost     = 0
        self.exec_time_ms  = 0
        self.replans       = 0

        self._build_ui()
        self._init_grid()

    # ──────────────────────────────────────────
    #  UI CONSTRUCTION
    # ──────────────────────────────────────────
    def _build_ui(self):
        # ── LEFT: Canvas area ──
        canvas_frame = tk.Frame(self.root, bg="#11111b")
        canvas_frame.pack(side=tk.LEFT, padx=12, pady=12)

        self.canvas = tk.Canvas(
            canvas_frame,
            bg=C_EMPTY,
            highlightthickness=0
        )
        self.canvas.pack()
        self.canvas.bind("<Button-1>",  self._on_click)
        self.canvas.bind("<B1-Motion>", self._on_click)

        # ── RIGHT: Control Panel (scrollable) ──
        panel_container = tk.Frame(self.root, bg="#181825", width=275)
        panel_container.pack(side=tk.RIGHT, fill=tk.Y)
        panel_container.pack_propagate(False)

        panel_canvas = tk.Canvas(panel_container, bg="#181825", highlightthickness=0, width=275)
        scrollbar = tk.Scrollbar(panel_container, orient="vertical", command=panel_canvas.yview)
        panel_canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        panel_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        panel = tk.Frame(panel_canvas, bg="#181825", width=255)
        panel_window = panel_canvas.create_window((0, 0), window=panel, anchor="nw")

        def _on_frame_configure(e):
            panel_canvas.configure(scrollregion=panel_canvas.bbox("all"))
        panel.bind("<Configure>", _on_frame_configure)

        def _on_mousewheel(e):
            panel_canvas.yview_scroll(int(-1*(e.delta/120)), "units")
        panel_canvas.bind_all("<MouseWheel>", _on_mousewheel)

        def section(text):
            tk.Label(panel, text=text, bg="#181825", fg="#7f849c",
                     font=("Courier", 9, "bold")).pack(anchor="w", padx=14, pady=(14,2))

        def styled_btn(parent, text, cmd, bg="#313244", fg=C_TEXT, bold=False):
            f = ("Courier", 10, "bold") if bold else ("Courier", 10)
            b = tk.Button(parent, text=text, command=cmd, bg=bg, fg=fg,
                          font=f, relief="flat", activebackground="#45475a",
                          activeforeground=C_TEXT, cursor="hand2", pady=6)
            b.pack(fill=tk.X, padx=14, pady=3)
            return b

        def labeled_combo(parent, label, values, var):
            tk.Label(parent, text=label, bg="#181825", fg="#7f849c",
                     font=("Courier", 9)).pack(anchor="w", padx=14)
            cb = ttk.Combobox(parent, textvariable=var, values=values,
                              state="readonly", font=("Courier", 10))
            cb.pack(fill=tk.X, padx=14, pady=3)
            return cb

        # Title
        tk.Label(panel, text="PATHFINDER", bg="#181825", fg=C_PATH,
                 font=("Courier", 16, "bold")).pack(pady=(18,2))
        tk.Label(panel, text="Dynamic Informed Search", bg="#181825", fg="#7f849c",
                 font=("Courier", 8)).pack()
        tk.Label(panel, text="By Raazia Mehmood 24F-0614", bg="#0f2747",
         fg=C_TEXT, font=("Courier", 9, "italic")).pack(pady=(0,8))

        # ── RUN / STOP always visible at top ──
        tk.Frame(panel, bg="#181825", height=8).pack()
        styled_btn(panel, "▶  RUN SEARCH", self._start_search,
                   bg=C_PATH, fg="#11111b", bold=True)
        styled_btn(panel, "■  STOP", self._stop_search, bg="#f38ba8", fg="#11111b")
        tk.Frame(panel, bg="#585b70", height=1).pack(fill=tk.X, padx=14, pady=6)

        # ── Grid Config ──
        section("GRID CONFIG")
        size_row = tk.Frame(panel, bg="#181825")
        size_row.pack(fill=tk.X, padx=14, pady=3)
        tk.Label(size_row, text="Rows:", bg="#181825", fg=C_TEXT,
                 font=("Courier", 10)).pack(side=tk.LEFT)
        self.rows_var = tk.IntVar(value=DEFAULT_ROWS)
        tk.Spinbox(size_row, from_=5, to=30, textvariable=self.rows_var,
                   width=4, font=("Courier", 10)).pack(side=tk.LEFT, padx=4)
        tk.Label(size_row, text="Cols:", bg="#181825", fg=C_TEXT,
                 font=("Courier", 10)).pack(side=tk.LEFT, padx=(8,0))
        self.cols_var = tk.IntVar(value=DEFAULT_COLS)
        tk.Spinbox(size_row, from_=5, to=30, textvariable=self.cols_var,
                   width=4, font=("Courier", 10)).pack(side=tk.LEFT, padx=4)

        styled_btn(panel, "Apply Grid Size", self._apply_grid_size)

        # Obstacle density
        dens_row = tk.Frame(panel, bg="#181825")
        dens_row.pack(fill=tk.X, padx=14, pady=3)
        tk.Label(dens_row, text="Wall %:", bg="#181825", fg=C_TEXT,
                 font=("Courier", 10)).pack(side=tk.LEFT)
        self.density_var = tk.IntVar(value=30)
        tk.Spinbox(dens_row, from_=0, to=70, textvariable=self.density_var,
                   width=4, font=("Courier", 10)).pack(side=tk.LEFT, padx=6)
        styled_btn(panel, "Generate Random Map", self._generate_random_map)

        # ── Mode Buttons ──
        section("EDITOR MODE")
        self.mode_btns = {}
        for label, mode, color in [
            ("Set Start (S)", "S",    C_START),
            ("Set Target (T)", "T",   C_TARGET),
            ("Draw Wall",      "Wall", C_OBSTACLE),
            ("Erase Wall",     "Erase","#a6adc8"),
        ]:
            b = styled_btn(panel, label, lambda m=mode: self._set_mode(m))
            b.config(fg=color)
            self.mode_btns[mode] = b

        # ── Algorithm Config ──
        section("ALGORITHM")
        self.algo_var = tk.StringVar(value="A*")
        labeled_combo(panel, "Search Strategy:",
                      ["A*", "Greedy Best-First (GBFS)"], self.algo_var)

        self.heuristic_var = tk.StringVar(value="Manhattan")
        labeled_combo(panel, "Heuristic Function:",
                      ["Manhattan", "Euclidean", "Chebyshev"], self.heuristic_var)

        # ── Dynamic Mode ──
        section("DYNAMIC MODE")
        self.dynamic_var = tk.BooleanVar(value=False)
        dyn_row = tk.Frame(panel, bg="#181825")
        dyn_row.pack(fill=tk.X, padx=14, pady=3)
        tk.Checkbutton(dyn_row, text="Enable Dynamic Obstacles",
                       variable=self.dynamic_var, bg="#181825", fg=C_TEXT,
                       selectcolor="#313244", activebackground="#181825",
                       font=("Courier", 10)).pack(side=tk.LEFT)

        prob_row = tk.Frame(panel, bg="#181825")
        prob_row.pack(fill=tk.X, padx=14, pady=2)
        tk.Label(prob_row, text="Spawn prob (%):", bg="#181825", fg=C_TEXT,
                 font=("Courier", 9)).pack(side=tk.LEFT)
        self.spawn_prob_var = tk.IntVar(value=10)
        tk.Spinbox(prob_row, from_=1, to=50, textvariable=self.spawn_prob_var,
                   width=4, font=("Courier", 10)).pack(side=tk.LEFT, padx=4)

        # ── Reset ──
        section("CONTROL")
        styled_btn(panel, "Clear Path", self._clear_path)
        styled_btn(panel, "Reset Grid", self._reset_grid)

        # ── Metrics Dashboard ──
        section("METRICS")
        self.metrics_frame = tk.Frame(panel, bg="#313244", relief="flat")
        self.metrics_frame.pack(fill=tk.X, padx=14, pady=4)

        self.metric_labels = {}
        for key, label in [
            ("algo",      "Algorithm"),
            ("heuristic", "Heuristic"),
            ("visited",   "Nodes Visited"),
            ("cost",      "Path Cost"),
            ("time",      "Exec Time (ms)"),
            ("replans",   "Re-plans"),
        ]:
            row = tk.Frame(self.metrics_frame, bg="#313244")
            row.pack(fill=tk.X, padx=8, pady=2)
            tk.Label(row, text=label+":", bg="#313244", fg="#7f849c",
                     font=("Courier", 9), width=16, anchor="w").pack(side=tk.LEFT)
            lbl = tk.Label(row, text="—", bg="#313244", fg=C_TEXT,
                           font=("Courier", 9, "bold"), anchor="w")
            lbl.pack(side=tk.LEFT)
            self.metric_labels[key] = lbl

        # ── Status ──
        self.status_lbl = tk.Label(panel, text="● Ready", bg="#181825",
                                   fg=C_START, font=("Courier", 10, "bold"))
        self.status_lbl.pack(pady=(12, 0))

        # ── Legend ──
        section("LEGEND")
        for color, label in [
            (C_START,    "Start Node"),
            (C_TARGET,   "Target Node"),
            (C_OBSTACLE, "Wall"),
            (C_FRONTIER, "Frontier (Open)"),
            (C_VISITED,  "Visited (Closed)"),
            (C_PATH,     "Final Path"),
            (C_AGENT,    "Agent"),
        ]:
            row = tk.Frame(panel, bg="#181825")
            row.pack(fill=tk.X, padx=14, pady=1)
            tk.Label(row, bg=color, width=2).pack(side=tk.LEFT, padx=(0,6))
            tk.Label(row, text=label, bg="#181825", fg=C_TEXT,
                     font=("Courier", 9)).pack(side=tk.LEFT)

    # ──────────────────────────────────────────
    #  GRID INITIALISATION
    # ──────────────────────────────────────────
    def _init_grid(self):
        self.canvas.config(
            width=self.cols * CELL_SIZE,
            height=self.rows * CELL_SIZE
        )
        self.canvas.delete("all")
        self.rects = {}
        self.grid = [[0]*self.cols for _ in range(self.rows)]

        for r in range(self.rows):
            for c in range(self.cols):
                x1 = c * CELL_SIZE
                y1 = r * CELL_SIZE
                rect = self.canvas.create_rectangle(
                    x1, y1, x1+CELL_SIZE, y1+CELL_SIZE,
                    fill=C_EMPTY, outline=C_GRID, width=1
                )
                self.rects[(r, c)] = rect

        # Restore start/target if they fit
        if self.start_pos and (self.start_pos[0] < self.rows and self.start_pos[1] < self.cols):
            self._paint(self.start_pos[0], self.start_pos[1], C_START, "S")
        else:
            self.start_pos = None

        if self.target_pos and (self.target_pos[0] < self.rows and self.target_pos[1] < self.cols):
            self._paint(self.target_pos[0], self.target_pos[1], C_TARGET, "T")
        else:
            self.target_pos = None

    def _apply_grid_size(self):
        self.rows = self.rows_var.get()
        self.cols = self.cols_var.get()
        self.start_pos  = None
        self.target_pos = None
        self._init_grid()
        self._set_status("Grid resized.", C_TEXT)

    def _generate_random_map(self):
        if not self.start_pos or not self.target_pos:
            messagebox.showwarning("Notice", "Place Start and Target first so they won't be walled in.")
        density = self.density_var.get() / 100.0
        for r in range(self.rows):
            for c in range(self.cols):
                if (r, c) == self.start_pos or (r, c) == self.target_pos:
                    continue
                if random.random() < density:
                    self.grid[r][c] = -1
                    self._paint(r, c, C_OBSTACLE)
                else:
                    self.grid[r][c] = 0
                    self._paint(r, c, C_EMPTY)
        self._set_status("Random map generated.", C_TEXT)

    # ──────────────────────────────────────────
    #  PAINTING / VISUAL HELPERS
    # ──────────────────────────────────────────
    def _paint(self, r, c, color, text=""):
        rect = self.rects.get((r, c))
        if rect is None:
            return
        self.canvas.itemconfig(rect, fill=color)
        tag = f"lbl_{r}_{c}"
        self.canvas.delete(tag)
        if text:
            x = c * CELL_SIZE + CELL_SIZE // 2
            y = r * CELL_SIZE + CELL_SIZE // 2
            fg = "#11111b" if color in (C_START, C_TARGET, C_FRONTIER, C_PATH, C_AGENT) else C_TEXT_DIM
            self.canvas.create_text(x, y, text=text, fill=fg,
                                    font=("Courier", 9, "bold"), tag=tag)

    def _update_metrics(self):
        self.metric_labels["algo"].config(text=self.algo_var.get())
        self.metric_labels["heuristic"].config(text=self.heuristic_var.get())
        self.metric_labels["visited"].config(text=str(self.nodes_visited))
        self.metric_labels["cost"].config(text=str(self.path_cost))
        self.metric_labels["time"].config(text=f"{self.exec_time_ms:.1f}")
        self.metric_labels["replans"].config(text=str(self.replans))

    def _set_status(self, msg, color=C_TEXT):
        self.status_lbl.config(text=f"● {msg}", fg=color)

    # ──────────────────────────────────────────
    #  EDITOR / CLICK HANDLING
    # ──────────────────────────────────────────
    def _set_mode(self, mode):
        self.mode = mode
        self._set_status(f"Mode: {mode}", C_FRONTIER)
        # Highlight active button
        for m, b in self.mode_btns.items():
            b.config(relief="sunken" if m == mode else "flat")

    def _on_click(self, event):
        if self.running:
            return
        c = event.x // CELL_SIZE
        r = event.y // CELL_SIZE
        if 0 <= r < self.rows and 0 <= c < self.cols:
            self._handle_cell(r, c)

    def _handle_cell(self, r, c):
        if self.mode == "S":
            if self.start_pos:
                self._paint(self.start_pos[0], self.start_pos[1], C_EMPTY)
                self.grid[self.start_pos[0]][self.start_pos[1]] = 0
            self.start_pos = (r, c)
            self.grid[r][c] = 0
            self._paint(r, c, C_START, "S")

        elif self.mode == "T":
            if self.target_pos:
                self._paint(self.target_pos[0], self.target_pos[1], C_EMPTY)
                self.grid[self.target_pos[0]][self.target_pos[1]] = 0
            self.target_pos = (r, c)
            self.grid[r][c] = 0
            self._paint(r, c, C_TARGET, "T")

        elif self.mode == "Wall":
            if (r, c) in (self.start_pos, self.target_pos):
                return
            self.grid[r][c] = -1
            self._paint(r, c, C_OBSTACLE)

        elif self.mode == "Erase":
            if (r, c) in (self.start_pos, self.target_pos):
                return
            self.grid[r][c] = 0
            self._paint(r, c, C_EMPTY)

    # ──────────────────────────────────────────
    #  GRID MANAGEMENT
    # ──────────────────────────────────────────
    def _reset_grid(self):
        self.running = False
        self.start_pos  = None
        self.target_pos = None
        self.current_path = []
        self.agent_pos    = None
        self.nodes_visited = 0
        self.path_cost     = 0
        self.exec_time_ms  = 0
        self.replans       = 0
        self._init_grid()
        self._update_metrics()
        self._set_status("Grid reset.", C_TEXT)

    def _clear_path(self):
        self.current_path = []
        self.agent_pos    = None
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] == -1:
                    continue
                if (r, c) == self.start_pos:
                    self._paint(r, c, C_START, "S")
                elif (r, c) == self.target_pos:
                    self._paint(r, c, C_TARGET, "T")
                else:
                    self._paint(r, c, C_EMPTY)

    # ──────────────────────────────────────────
    #  NEIGHBOUR GENERATION
    # ──────────────────────────────────────────
    def _get_h(self, r, c):
        gr, gc = self.target_pos
        h_name = self.heuristic_var.get()
        if h_name == "Manhattan":
            return heuristic_manhattan(r, c, gr, gc)
        elif h_name == "Euclidean":
            return heuristic_euclidean(r, c, gr, gc)
        else:
            return heuristic_chebyshev(r, c, gr, gc)

    def _get_move_cost(self, dr, dc):
        """Diagonal moves cost √2, cardinal moves cost 1."""
        return 1.414 if (dr, dc) in DIAGONAL_MOVES else 1.0

    def _get_neighbors(self, node):
        neighbors = []
        for dr, dc in MOVES:
            nr, nc = node.r + dr, node.c + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                if self.grid[nr][nc] != -1:
                    step_cost = self._get_move_cost(dr, dc)
                    g = node.g + step_cost
                    h = self._get_h(nr, nc)
                    neighbors.append(Node(nr, nc, node, g, h))
        return neighbors

    # ──────────────────────────────────────────
    #  SEARCH ALGORITHMS
    # ──────────────────────────────────────────
    def _search(self, start_r, start_c):
        """
        Unified search dispatcher.
        Returns the goal Node with parent chain, or None.
        Handles both A* and GBFS.
        """
        algo = self.algo_var.get()
        h0   = self._get_h(start_r, start_c)
        start_node = Node(start_r, start_c, None, g=0, h=h0)

        # Priority queue: (priority, tie-breaker, Node)
        open_heap  = []
        counter    = 0  # tie-breaker

        if algo == "A*":
            start_node.f = start_node.g + start_node.h
        else:  # GBFS
            start_node.f = start_node.h

        heapq.heappush(open_heap, (start_node.f, counter, start_node))

        # open_set for fast membership check
        open_set   = {(start_r, start_c): start_node.f}
        closed_set = set()

        while open_heap and self.running:
            _, _, curr = heapq.heappop(open_heap)
            pos = curr.pos()

            if pos in closed_set:
                continue

            closed_set.add(pos)
            self.nodes_visited += 1

            # Visualise visited (but not start or target)
            if pos != self.start_pos and pos != self.target_pos:
                self._paint(curr.r, curr.c, C_VISITED, str(self.nodes_visited))
                self.root.update()
                time.sleep(ANIMATION_DELAY)

            if pos == self.target_pos:
                return curr

            for nb in self._get_neighbors(curr):
                nb_pos = nb.pos()
                if nb_pos in closed_set:
                    continue

                if algo == "A*":
                    nb.f = nb.g + nb.h
                else:
                    nb.f = nb.h

                if nb_pos not in open_set or nb.f < open_set[nb_pos]:
                    open_set[nb_pos] = nb.f
                    counter += 1
                    heapq.heappush(open_heap, (nb.f, counter, nb))
                    # Visualise frontier
                    if nb_pos != self.target_pos:
                        self._paint(nb.r, nb.c, C_FRONTIER)

        return None  # No path found

    def _extract_path(self, goal_node):
        """Walk parent chain → return list of (r, c) from start to goal."""
        path = []
        curr = goal_node
        while curr:
            path.append(curr.pos())
            curr = curr.parent
        path.reverse()
        return path

    def _draw_path(self, path):
        for r, c in path:
            if (r, c) != self.start_pos and (r, c) != self.target_pos:
                self._paint(r, c, C_PATH)

    # ──────────────────────────────────────────
    #  DYNAMIC OBSTACLE LOGIC
    # ──────────────────────────────────────────
    def _spawn_obstacle(self):
        """
        Randomly spawns a wall with probability spawn_prob.
        Returns True if an obstacle was placed ON the current remaining path.
        """
        prob = self.spawn_prob_var.get() / 100.0
        if random.random() > prob:
            return False

        # Pick a random empty cell that is NOT start, target, or agent
        candidates = [
            (r, c) for r in range(self.rows) for c in range(self.cols)
            if self.grid[r][c] == 0
            and (r, c) != self.start_pos
            and (r, c) != self.target_pos
            and (r, c) != self.agent_pos
        ]
        if not candidates:
            return False

        r, c = random.choice(candidates)
        self.grid[r][c] = -1
        self._paint(r, c, C_OBSTACLE)

        # Check if it blocks the current path
        return (r, c) in self.current_path

    # ──────────────────────────────────────────
    #  AGENT ANIMATION WITH RE-PLANNING
    # ──────────────────────────────────────────
    def _animate_agent(self, path):
        """
        Move the agent step-by-step along `path`.
        In Dynamic Mode: after each step, possibly spawn an obstacle
        and re-plan if the path is blocked.
        """
        self.current_path = path[:]
        idx = 0  # current position index in path

        while idx < len(self.current_path) - 1 and self.running:
            r, c = self.current_path[idx]
            self.agent_pos = (r, c)

            # Paint agent dot
            if (r, c) != self.start_pos and (r, c) != self.target_pos:
                self._paint(r, c, C_AGENT, "●")
            self.root.update()
            time.sleep(ANIMATION_DELAY * 2)

            # Clean behind agent
            if (r, c) != self.start_pos:
                self._paint(r, c, C_PATH)  # leave path trail

            # Dynamic Mode: possibly spawn obstacle
            if self.dynamic_var.get():
                blocked = self._spawn_obstacle()
                if blocked:
                    # Re-plan from current position
                    next_r, next_c = self.current_path[idx + 1]
                    self._set_status("Obstacle! Re-planning...", C_FRONTIER)
                    self.root.update()

                    # Clear old future path visualization
                    for fr, fc in self.current_path[idx+1:]:
                        if (fr, fc) != self.target_pos:
                            self._paint(fr, fc, C_EMPTY)

                    self.nodes_visited = 0  # reset for new plan
                    t0 = time.perf_counter()
                    goal_node = self._search(r, c)
                    self.exec_time_ms = (time.perf_counter() - t0) * 1000
                    self.replans += 1

                    if goal_node is None:
                        self._set_status("No path after obstacle! Stopped.", C_OBSTACLE)
                        self._update_metrics()
                        return

                    new_path = self._extract_path(goal_node)
                    self._draw_path(new_path)
                    self.current_path = new_path
                    self.path_cost = len(new_path) - 1
                    idx = 0
                    self._update_metrics()
                    continue

            idx += 1

        # Reached target
        tr, tc = self.target_pos
        self._paint(tr, tc, C_TARGET, "T")
        self._set_status("Target Reached!", C_START)

    # ──────────────────────────────────────────
    #  MAIN SEARCH ENTRY POINT
    # ──────────────────────────────────────────
    def _start_search(self):
        if not self.start_pos or not self.target_pos:
            messagebox.showerror("Error", "Place both Start (S) and Target (T) first.")
            return

        self._clear_path()
        self.running       = True
        self.nodes_visited = 0
        self.path_cost     = 0
        self.exec_time_ms  = 0
        self.replans       = 0
        self.agent_pos     = self.start_pos
        self._set_status("Searching...", C_FRONTIER)
        self._update_metrics()

        t_start = time.perf_counter()
        goal_node = self._search(self.start_pos[0], self.start_pos[1])
        self.exec_time_ms = (time.perf_counter() - t_start) * 1000

        if not self.running:
            self._set_status("Stopped.", "#f38ba8")
            return

        if goal_node is None:
            self._set_status("No path found.", C_OBSTACLE)
            self._update_metrics()
            self.running = False
            return

        path = self._extract_path(goal_node)
        self.path_cost = len(path) - 1
        self._draw_path(path)
        self._update_metrics()
        self._set_status("Path found! Animating agent...", C_PATH)
        self.root.update()
        time.sleep(0.4)

        # Animate the agent moving
        self._animate_agent(path)
        self._update_metrics()
        self.running = False

    def _stop_search(self):
        self.running = False
        self._set_status("Stopped.", "#f38ba8")


# ─────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(False, False)
    app = DynamicPathfinderApp(root)
    root.mainloop()
