import tkinter as tk
import random
from tkinter import messagebox
import json
from minesweeper import Minesweeper

class Liar(Minesweeper):
    def __init__(self, master, rows, cols, mines, load_main_menu, enable_timer):
        super().__init__(master, rows, cols, mines, load_main_menu, enable_timer)

    def Rule_Click(self):
        messagebox.showinfo("Rule", "The number of the clue always overshoot or undershoot the true value E.g. If the clue says 2, the actual number of surrounding mine could be either 1 or 3.")

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

    def continue_game(self):
        try:
            with open('game_state.json', 'r') as f:
                game_state = json.load(f)

            self.rows = game_state['rows']
            self.cols = game_state['cols']
            self.mines = game_state['mines']
            self.grid = game_state['grid']
            self.revealed = game_state['revealed']
            self.flagged = game_state['flagged']

            self.frame.destroy()
            self.create_widgets()

            for r in range(self.rows):
                for c in range(self.cols):
                    if self.revealed[r][c]:
                        self.buttons[(r, c)].config(relief=tk.SUNKEN, state=tk.DISABLED)
                        if self.grid[r][c] == -1:
                            self.buttons[(r, c)].config(text="M", bg="red")
                        elif self.grid[r][c] > 0:
                            self.buttons[(r, c)].config(text=str(self.grid[r][c]))
                        else:
                            self.buttons[(r, c)].config(text="0")
                    elif self.flagged[r][c]:
                        self.buttons[(r, c)].config(text="F")
                        self.flags += 1


            self.mine_count_label.config(text=f"Mines: {self.mines - self.flags}")

        except FileNotFoundError:
            messagebox.showinfo("Minesweeper", "No saved game to continue.")
        except Exception as e:
            messagebox.showerror("Minesweeper", f"Failed to load game state: {e}")
