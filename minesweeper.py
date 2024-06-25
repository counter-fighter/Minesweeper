import random
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

selectionbar_color = '#eff5f6'
sidebar_color = '#F5E1FD'
header_color = '#53366b'
visualisation_frame_color = "#ffffff"

class Minesweeper:
    def __init__(self, master, rows, cols, mines):
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

class MainMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Minesweeper Menu")
        
        # Configure style
        style = ttk.Style()
        self.root.configure(background='#2E4053')
        style.configure("TLabel", font=("Helvetica", 12), background='#2E4053', foreground='#FDFEFE')
        style.configure("TRadiobutton", font=("Helvetica", 12), background='#2E4053', foreground='#FDFEFE', indicatoron=0)
        style.configure("TCheckbutton", font=("Helvetica", 12), background='#2E4053', foreground='#FDFEFE')
        style.configure("TButton", font=("Helvetica", 12, "bold"), background='#1ABC9C', foreground='#2E4053')
        
        # Set styles for hover effects
        style.map("TButton",
                  background=[('active', '#16A085')],
                  foreground=[('active', '#ECF0F1')])
        style.map("TRadiobutton",
                  background=[('selected', '#1ABC9C')],
                  foreground=[('selected', '#2E4053')])
        
        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding="20 20 20 20", style="TFrame")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Board size options
        self.board_size_var = tk.IntVar(value=5)
        board_size_label = ttk.Label(self.main_frame, text="Select Board Size:")
        board_size_label.grid(row=0, column=0, sticky=tk.W, pady=5)
        board_sizes = ["Small", "Medium", "Large"]
        for index, size in enumerate(board_sizes):
            ttk.Radiobutton(self.main_frame, text=size, variable=self.board_size_var, value=5 * (2 ** index)).grid(row=0, column=1+index, sticky=tk.W, padx=5)
        
        # Difficulty level options
        self.difficulty_var = tk.DoubleVar(value=0.1)
        difficulty_label = ttk.Label(self.main_frame, text="Select Difficulty Level:")
        difficulty_label.grid(row=1, column=0, sticky=tk.W, pady=5)
        difficulty_levels = ["Easy", "Medium", "Hard"]
        for index, level in enumerate(difficulty_levels):
            ttk.Radiobutton(self.main_frame, text=level, variable=self.difficulty_var, value=0.1 + index*0.05).grid(row=1, column=1+index, sticky=tk.W, padx=5)
        
        # Timer toggle
        self.timer_var = tk.BooleanVar(value=False)
        timer_label = ttk.Label(self.main_frame, text="Enable Timer:")
        timer_label.grid(row=2, column=0, sticky=tk.W, pady=5)
        timer_toggle = ttk.Checkbutton(self.main_frame, variable=self.timer_var)
        timer_toggle.grid(row=2, column=1, sticky=tk.W, padx=5)
        
        # Start button
        start_button = ttk.Button(self.main_frame, text="Start Game", command=self.start_game)
        start_button.grid(row=3, column=0, columnspan=4, pady=20)
        
        # Add some spacing
        for child in self.main_frame.winfo_children():
            child.grid_configure(padx=5, pady=5)
    
    def get_mines(self):
        print(self.board_size_var.get(), self.difficulty_var.get())
        return int(self.board_size_var.get() * self.board_size_var.get() * self.difficulty_var.get())

    def start_game(self):
        timer_enabled = self.timer_var.get()
        self.main_frame.destroy()
        Minesweeper(self.root, self.board_size_var.get(), self.board_size_var.get(), self.get_mines())