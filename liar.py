import tkinter as tk
from tkinter import messagebox
import random

class Minesweeper:
    def __init__(self, master, rows=10, cols=10, mines=10):
        self.master = master
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.buttons = {}
        self.flags = 0
        self.create_widgets()
        self.setup_game()

    def create_widgets(self):
        self.frame = tk.Frame(self.master)
        self.frame.pack()
        self.mine_count_label = tk.Label(self.master, text=f"Mines: {self.mines}")
        self.mine_count_label.pack()
        for r in range(self.rows):
            for c in range(self.cols):
                button = tk.Button(self.frame, width=2, height=1, command=lambda r=r, c=c: self.on_left_click(r, c))
                button.bind("<Button-3>", lambda event, r=r, c=c: self.on_right_click(r, c))
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
                # Adjust the count by ±1
                if count > 0:
                    adjustment = random.choice([-1, 1])
                    count += adjustment
                self.grid[r][c] = max(0, count)

    def on_left_click(self, r, c):
        if self.flagged[r][c] or self.revealed[r][c]:
            return
        if self.grid[r][c] == -1:
            self.reveal_cell(r, c)
            self.game_over(False)
        else:
            self.reveal_cell(r, c)
            if self.check_win():
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
            #Change to this line as well
            self.buttons[(r, c)].config(text="0")
            for i in range(max(0, r-1), min(self.rows, r+2)):
                for j in range(max(0, c-1), min(self.cols, c+2)):
                    #Change on this line
                    if self.grid[i][j] != -1 and not self.revealed[i][j]:
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

class MainMenu:
    def __init__(self, master):
        self.master = master
        self.master.title("Minesweeper Main Menu")
        self.frame = tk.Frame(self.master)
        self.frame.pack(pady=20)

        self.board_size_label = tk.Label(self.frame, text="Board Size:")
        self.board_size_label.grid(row=0, column=0, padx=5, pady=5)
        self.board_size_var = tk.IntVar(value=10)
        self.board_size_entry = tk.Entry(self.frame, textvariable=self.board_size_var)
        self.board_size_entry.grid(row=0, column=1, padx=5, pady=5)

        self.mines_label = tk.Label(self.frame, text="Number of Mines:")
        self.mines_label.grid(row=1, column=0, padx=5, pady=5)
        self.mines_var = tk.IntVar(value=20)
        self.mines_entry = tk.Entry(self.frame, textvariable=self.mines_var)
        self.mines_entry.grid(row=1, column=1, padx=5, pady=5)

        self.play_button = tk.Button(self.frame, text="Play", command=self.start_game)
        self.play_button.grid(row=2, columnspan=2, pady=20)

    def start_game(self):
        rows = self.board_size_var.get()
        cols = self.board_size_var.get()
        mines = self.mines_var.get()
        self.frame.destroy()
        Minesweeper(self.master, rows, cols, mines)

if __name__ == "__main__":
    root = tk.Tk()
    main_menu = MainMenu(root)
    root.mainloop()