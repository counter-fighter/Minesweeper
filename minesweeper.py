import json
import random
import time, datetime
import tkinter as tk
from tkinter import messagebox

selectionbar_color = '#eff5f6'
sidebar_color = '#F5E1FD'
header_color = '#53366b'
visualisation_frame_color = "#ffffff"

class Minesweeper:
    def __init__(self, master, rows=10, cols=10, mines=10, load_main_menu=None, enable_timer=False):
        self.master = master
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.buttons = {}
        self.flags = 0
        self.mine_count_label = None
        self.create_widgets()
        self.setup_game()
        self.load_main_menu = load_main_menu
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)
        self.done = False
        self.enable_timer = enable_timer
        if self.enable_timer:
            self.status = tk.Label(self.master, text='')
            self.status.grid(row=self.rows, column=0, columnspan=self.cols)
            self.start_time = time.time()
            self.elapsed_time = 0
            self.update_status()

    def create_widgets(self):
        # Set up frame
        self.frame = tk.Frame(self.master)
        self.frame.grid(row=1, column=0, columnspan=10)
        # Add help menu
        self.menu_bar = tk.Menu(self.master)
        self.master.config(menu=self.menu_bar)
        help_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.menu_bar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Return to Main Menu", command=self.Main_Menu_Click)
        help_menu.add_command(label="Rule", command=self.Rule_Click)
        # Add Mine Count
        if self.mine_count_label is None:
            self.mine_count_label = tk.Label(self.master, text=f"Mines: {self.mines}")
            self.mine_count_label.grid(row=self.rows + 1, column=0, columnspan=self.cols, padx=50, pady=5)
        else:
            self.mine_count_label.config(text=f"Mines: {self.mines}")
        #Set up button
        for r in range(self.rows):
            for c in range(self.cols):
                button = tk.Button(self.frame, width=2, height=1, command=lambda r=r, c=c: self.on_left_click(r, c))
                button.bind("<Button-3>", lambda event, r=r, c=c: self.on_right_click(r, c))
                # For Highlight Clue
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
            self.done = True
            self.game_over(False)
        elif self.check_win():
            self.done = True
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
            #Recursively reveal the surrounding cell if the other cell is also empty (stop when the cell is not empty)
            self.buttons[(r, c)].config(text="")
            for i in range(max(0, r-1), min(self.rows, r+2)):
                for j in range(max(0, c-1), min(self.cols, c+2)):
                    if not self.revealed[i][j]:
                        self.reveal_cell(i, j)

    # To Highlight Clue
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
        self.save_state_and_destroy()

    def Main_Menu_Click(self):
        self.done = True
        self.save_state_and_destroy()
    
    def save_state_and_destroy(self):
        self.save_game_state()    
        self.frame.destroy()
        if self.enable_timer: self.status.destroy()
        self.mine_count_label.destroy()
        self.menu_bar.destroy()
        self.load_main_menu(self.master)

    def Rule_Click(self):
        messagebox.showinfo("Rule", "Some of these squares are a mine. If you click a mine, you lose. You can reveal a tile by left click and flagged that tile as a mine by right click. The number of the clue indicates how many mines in the 8 adjacent squares. Use logical deductions to determine which tile is safe to click and which tile to flag. Good luck :D")

    def on_close(self):
        self.save_game_state()
        self.master.destroy()

    def save_game_state(self):
        game_state = {
            'rows': self.rows,
            'cols': self.cols,
            'mines': self.mines,
            'grid': self.grid,
            'revealed': self.revealed,
            'flagged': self.flagged
        }
        with open('game_state.json', 'w') as f:
            json.dump(game_state, f)

    def load_game_state(self):
        try:
            with open('game_state.json', 'r') as f:
                game_state = json.load(f)
            self.rows = game_state['rows']
            self.cols = game_state['cols']
            self.mines = game_state['mines']
            self.grid = game_state['grid']
            self.revealed = game_state['revealed']
            self.flagged = game_state['flagged']
        except FileNotFoundError:
            pass

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
                            self.buttons[(r, c)].config(text="")
                    elif self.flagged[r][c]:
                        self.buttons[(r, c)].config(text="F")
                        self.flags += 1

            self.mine_count_label.config(text=f"Mines: {self.mines - self.flags}")

        except FileNotFoundError:
            messagebox.showinfo("Minesweeper", "No saved game to continue.")
        except Exception as e:
            messagebox.showerror("Minesweeper", f"Failed to load game state: {e}")
  
    def update_status(self):
        self.elapsed_time = int(time.time() - self.start_time)
        delta = str(datetime.timedelta(seconds=self.elapsed_time))
        if not self.done:
            self.status.config(text='Timer: 'f'{delta}')
            self.master.after(1000, self.update_status)  # Run again after 1 second
