import random
import time
import tkinter as tk
from tkinter import messagebox


selectionbar_color = '#eff5f6'
sidebar_color = '#F5E1FD'
header_color = '#53366b'
visualisation_frame_color = "#ffffff"

class Minesweeper:
    def __init__(self, master, rows, cols, mines, load_main_menu):
        self.master = master
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.buttons = {}
        self.flags = 0
        self.create_widgets()
        self.setup_game()
        self.load_main_menu = load_main_menu

    def create_widgets(self):
        self.frame = tk.Frame(self.master)
        self.frame.pack()
        self.mine_count_label = tk.Label(self.master, text=f"Mines: {self.mines}")
        self.mine_count_label.pack()
        for r in range(self.rows):
            for c in range(self.cols):
                button = tk.Button(self.frame, width=2, height=1, command=lambda r=r, c=c: self.on_left_click(r, c))
                button.bind("<Button-3>", lambda event, r=r, c=c: self.on_right_click(r, c))
                button.bind("<Enter>", lambda event, r=r, c=c: self.on_enter(r, c))
                button.bind("<Leave>", lambda event, r=r, c=c: self.on_leave(r, c))
                button.grid(row=r, column=c)
                self.buttons[(r, c)] = button

    def setup_game(self):
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.revealed = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        self.flagged = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        self.place_mines()
        self.calculate_numbers()

    def place_mines(self):
        mines_placed = 0
        while mines_placed < self.mines:
            r = random.randint(0, self.rows - 1)
            c = random.randint(0, self.cols - 1)
            if self.grid[r][c] != -1:
                self.grid[r][c] = -1
                mines_placed += 1

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
                self.grid[r][c] = count

    def on_left_click(self, r, c):
        if self.flagged[r][c] or self.revealed[r][c]:
            return
        self.reveal_cell(r, c)
        if self.grid[r][c] == -1:
            self.game_over(False)
        elif self.check_win():
            self.game_over(True)

    def on_right_click(self, r, c):
        if self.revealed[r][c]:
            return
        if self.flagged[r][c]:
            self.buttons[(r, c)].config(text="")
            self.flagged[r][c] = False
            self.flags -= 1
        else:
            self.buttons[(r, c)].config(text="F")
            self.flagged[r][c] = True
            self.flags += 1
        self.mine_count_label.config(text=f"Mines: {self.mines - self.flags}")

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
            self.buttons[(r, c)].config(text="")
            for i in range(max(0, r-1), min(self.rows, r+2)):
                for j in range(max(0, c-1), min(self.cols, c+2)):
                    if not self.revealed[i][j]:
                        self.reveal_cell(i, j)

    def check_win(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] != -1 and not self.revealed[r][c]:
                    return False
        return True

    def game_over(self, won):
        for r in range(self.rows):
            for c in range(self.cols):
                self.buttons[(r, c)].config(state=tk.DISABLED)
                if self.grid[r][c] == -1:
                    self.buttons[(r, c)].config(text="M")
        if won:
            messagebox.showinfo("Minesweeper", "Congratulations, You won!")
        else:
            messagebox.showinfo("Minesweeper", "Game Over. You hit a mine.")
        self.frame.destroy()
        self.mine_count_label.destroy()
        self.load_main_menu(self.master)

    def on_enter(self, r, c):
        if self.revealed[r][c]:
            for i in range(max(0, r-1), min(self.rows, r+2)):
                for j in range(max(0, c-1), min(self.cols, c+2)):
                    if not self.revealed[i][j]:
                        self.buttons[(i, j)].config(bg="darkgray")

    def on_leave(self, r, c):
        if self.revealed[r][c]:
            for i in range(max(0, r-1), min(self.rows, r+2)):
                for j in range(max(0, c-1), min(self.cols, c+2)):
                    if not self.revealed[i][j]:
                        self.buttons[(i, j)].config(bg="SystemButtonFace")
