import tkinter as tk
import random
from collections import deque

CELL_SIZE = 25
ROWS = 21
COLS = 21

class MazeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Maze Solver Visualizer")

        self.canvas = tk.Canvas(root, width=COLS*CELL_SIZE, height=ROWS*CELL_SIZE)
        self.canvas.pack()

        self.grid = [[0]*COLS for _ in range(ROWS)]
        self.start = (0, 0)
        self.end = (ROWS-1, COLS-1)

        self.create_buttons()
        self.generate_maze()

    def create_buttons(self):
        frame = tk.Frame(self.root)
        frame.pack()

        tk.Button(frame, text="Generate Maze", command=self.generate_maze).pack(side=tk.LEFT)
        tk.Button(frame, text="Solve BFS", command=self.solve_bfs).pack(side=tk.LEFT)
        tk.Button(frame, text="Solve DFS", command=self.solve_dfs).pack(side=tk.LEFT)
        tk.Button(frame, text="Reset", command=self.reset).pack(side=tk.LEFT)

    def draw_grid(self):
        self.canvas.delete("all")
        for r in range(ROWS):
            for c in range(COLS):
                x1, y1 = c*CELL_SIZE, r*CELL_SIZE
                x2, y2 = x1+CELL_SIZE, y1+CELL_SIZE

                color = "black" if self.grid[r][c] == 0 else "white"
                if (r, c) == self.start:
                    color = "blue"
                elif (r, c) == self.end:
                    color = "red"

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")

    def generate_maze(self):
        self.grid = [[0]*COLS for _ in range(ROWS)]

        def carve(r, c):
            dirs = [(0,2),(2,0),(0,-2),(-2,0)]
            random.shuffle(dirs)
            for dr, dc in dirs:
                nr, nc = r+dr, c+dc
                if 0 <= nr < ROWS and 0 <= nc < COLS and self.grid[nr][nc] == 0:
                    self.grid[nr][nc] = 1
                    self.grid[r+dr//2][c+dc//2] = 1
                    carve(nr, nc)

        self.grid[0][0] = 1
        carve(0, 0)
        self.grid[ROWS-1][COLS-1] = 1

        self.draw_grid()

    def animate_cell(self, r, c, color):
        x1, y1 = c*CELL_SIZE, r*CELL_SIZE
        x2, y2 = x1+CELL_SIZE, y1+CELL_SIZE
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")
        self.root.update()
        self.root.after(20)

    def solve_bfs(self):
        q = deque([(self.start[0], self.start[1], [self.start])])
        visited = set([self.start])

        while q:
            r, c, path = q.popleft()

            if (r, c) != self.start:
                self.animate_cell(r, c, "yellow")

            if (r, c) == self.end:
                for pr, pc in path:
                    self.animate_cell(pr, pc, "green")
                return

            for dr, dc in [(0,1),(1,0),(0,-1),(-1,0)]:
                nr, nc = r+dr, c+dc
                if 0 <= nr < ROWS and 0 <= nc < COLS:
                    if self.grid[nr][nc] == 1 and (nr, nc) not in visited:
                        visited.add((nr, nc))
                        q.append((nr, nc, path + [(nr, nc)]))

    def solve_dfs(self):
        stack = [(self.start[0], self.start[1], [self.start])]
        visited = set([self.start])

        while stack:
            r, c, path = stack.pop()

            if (r, c) != self.start:
                self.animate_cell(r, c, "orange")

            if (r, c) == self.end:
                for pr, pc in path:
                    self.animate_cell(pr, pc, "green")
                return

            for dr, dc in [(0,1),(1,0),(0,-1),(-1,0)]:
                nr, nc = r+dr, c+dc
                if 0 <= nr < ROWS and 0 <= nc < COLS:
                    if self.grid[nr][nc] == 1 and (nr, nc) not in visited:
                        visited.add((nr, nc))
                        stack.append((nr, nc, path + [(nr, nc)]))

    def reset(self):
        self.draw_grid()


# Run App
root = tk.Tk()
app = MazeGUI(root)
root.mainloop()