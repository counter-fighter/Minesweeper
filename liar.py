import tkinter as tk
from tkinter import messagebox
import random
from minesweeper import MainMenu, Minesweeper

class Liar(Minesweeper):
    def __init__(self, master, rows, cols, mines):
        super().__init__(master, rows, cols, mines)

    def calculate_numbers(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] == -1:
                    continue
                count = 0
                for i in range(max(0, r-1), min(self.rows, r+2)):
                    for j in range(max(0, c-1), min(self.cols, c+2)):
                        if self.grid[i][j] == -1:
                            count += 1
                # Adjust the count by ±1
                if count > 0:
                    adjustment = random.choice([-1, 1])
                    count += adjustment
                self.grid[r][c] = max(0, count)

    def reveal_cell(self, r, c):
        if self.revealed[r][c] or self.flagged[r][c]:
            return
        self.revealed[r][c] = True
        self.buttons[(r, c)].config(relief=tk.SUNKEN, state=tk.DISABLED)
        if self.grid[r][c] == -1:
            self.buttons[(r, c)].config(text="M", bg="red")
        elif self.grid[r][c] > 0:
            self.buttons[(r, c)].config(text=str(self.grid[r][c]))
        else:
            self.buttons[(r, c)].config(text="0")
            for i in range(max(0, r-1), min(self.rows, r+2)):
                for j in range(max(0, c-1), min(self.cols, c+2)):
                    if self.grid[i][j] != -1 and not self.revealed[i][j]:
                        self.reveal_cell(i, j)

class LiarM(MainMenu):
    def __init__(self, master):
        super().__init__(master)

    def start_game(self):
        rows = self.board_size_var.get()
        cols = self.board_size_var.get()
        mines = self.mines_var.get()
        self.frame.destroy()
        Liar(self.master, rows, cols, mines)
