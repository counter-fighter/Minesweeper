import tkinter as tk
from tkinter import messagebox
from minesweeper import Minesweeper

class vnh_clue(Minesweeper):
    def __init__(self, master, rows, cols, mines, load_main_menu, enable_timer):
        super().__init__(master, rows, cols, mines, load_main_menu, enable_timer)

    def Rule_Click(self):
        messagebox.showinfo("Rule", "The clue refers to the tiles vertically and horizontally in the range of 2 tiles away from the number instead of the surrounding tiles.")

    def calculate_numbers(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] == -1:
                    continue
                count = 0
                for i in range(max(0, r-2), min(self.rows, r+3)):
                    if i != r and self.grid[i][c] == -1:
                        count += 1
                for j in range(max(0, c-2), min(self.cols, c+3)):
                    if j != c and self.grid[r][j] == -1:
                        count += 1
                self.grid[r][c] = count

    def on_enter(self, r, c):
        if self.revealed[r][c]:
            #For vertucal tile
            for i in range(max(0, r-2), min(self.rows, r+3)):
                if not self.revealed[i][c] and i != r:
                    self.buttons[(i, c)].config(bg="darkgray")
            #For Horizontal tile
            for j in range(max(0, c-2), min(self.cols, c+3)):
                if not self.revealed[r][j] and j != c:
                    self.buttons[(r, j)].config(bg="darkgray")

    def on_leave(self, r, c):
        if self.revealed[r][c]:
            for i in range(max(0, r-2), min(self.rows, r+3)):
                if not self.revealed[i][c] and i != r:
                    self.buttons[(i, c)].config(bg="SystemButtonFace")
            for j in range(max(0, c-2), min(self.cols, c+3)):
                if not self.revealed[r][j] and j != c:
                    self.buttons[(r, j)].config(bg="SystemButtonFace")

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
            #Change this part so that the function recursively reveal a tile in a + shape instead of the surrounding tile
            self.buttons[(r, c)].config(text="")
            for i in range(max(0, r-2), min(self.cols, r+3)):
                if i != r and not self.revealed[i][c]:
                    self.reveal_cell(i, c)
            for j in range(max(0, c-2), min(self.cols, c+3)):
                if j != c and not self.revealed[r][j]:
                    self.reveal_cell(r, j)
