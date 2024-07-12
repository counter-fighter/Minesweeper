import tkinter as tk
from tkinter import messagebox
from minesweeper import Minesweeper

class TwoTilesAway(Minesweeper):
    def __init__(self, master, rows, cols, mines, load_main_menu, enable_timer):
        super().__init__(master, rows, cols, mines, load_main_menu, enable_timer)

    def Rule_Click(self):
        messagebox.showinfo("Rule", "The mines are hidden two tiles away from the number of the clue.")

    def calculate_numbers(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] == -1:
                    continue
                count = 0
                for i in range(max(0, r-2), min(self.rows, r+3)):
                    for j in range(max(0, c-2), min(self.cols, c+3)):
                        if self.grid[i][j] == -1:
                            count += 1
                self.grid[r][c] = count

    def on_enter(self, r, c):
        if self.revealed[r][c]:
            for i in range(max(0, r-2), min(self.rows, r+3)):
                for j in range(max(0, c-2), min(self.cols, c+3)):
                    if not self.revealed[i][j]:
                        self.buttons[(i, j)].config(bg="darkgray")

    def on_leave(self, r, c):
        if self.revealed[r][c]:
            for i in range(max(0, r-2), min(self.rows, r+3)):
                for j in range(max(0, c-2), min(self.cols, c+3)):
                    if not self.revealed[i][j]:
                        self.buttons[(i, j)].config(bg="SystemButtonFace")

