import tkinter as tk
from tkinter import ttk, messagebox
import json
from os.path import exists
from os import getcwd
from minesweeper import Minesweeper
from liar import Liar
from two_tiles_away import TwoTilesAway
from vnh_clue import vnh_clue

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
        style.configure("TButton", font=("Helvetica", 12, "bold"), background='#000000', foreground='#2E4053')
        style.configure("Red.TButton", font=("Helvetica", 12, "bold"), background='#FF0000', foreground='#2E4053')
        style.configure("Green.TButton", font=("Helvetica", 12, "bold"), background='#00CC00', foreground='#2E4053')

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
        start_button = ttk.Button(self.main_frame, text="New Game", command=self.start_game)
        start_button.grid(row=4, column=1, pady=20, padx=5, sticky=tk.EW)
        # Add Continue Game
        continue_button = ttk.Button(self.main_frame, text="Continue", command=self.continue_game, style = "Green.TButton")
        continue_button.grid(row=4, column=2, pady=20, padx=5, sticky=tk.EW)
        # Add Quit Button
        quit_button = ttk.Button(self.main_frame, text="Quit", command=self.quit_game, style="Red.TButton")
        quit_button.grid(row=4, column=3, pady=20, padx=5, sticky=tk.EW)

        
        file_path = str(getcwd()) + '\\game_state.json'
        file_path_fwd = str(getcwd()) + '/game_state.json'
        
        if not (exists(file_path) or exists(file_path_fwd)):
            continue_button.state(["disabled"])
        else:
            continue_button.state(["!disabled"])

        # Add some spacing
        for child in self.main_frame.winfo_children():
            child.grid_configure(padx=5, pady=5)
        
        # Add modes
        self.mode = tk.StringVar(value="Classic")
        mode_label = ttk.Label(self.main_frame, text="Select Game Mode")
        mode_label.grid(row=3, column=0, sticky=tk.W, pady=5)
        mode_options = ["Classic", "Liar", "Two Tiles Away","Vertical and Horizontal Clue"]
        for index, mode in enumerate(mode_options):
            ttk.Radiobutton(self.main_frame, text=mode, variable=self.mode, value=mode).grid(row=3, column=1+index, sticky=tk.W, padx=5)
    
    def get_mines(self):
        return int(self.board_size_var.get() * self.board_size_var.get() * self.difficulty_var.get())

    def start_game(self):
        timer_enabled = self.timer_var.get()
        self.main_frame.destroy()
        match self.mode.get():
            case "Classic":
                Minesweeper(self.root, timer_enabled, self.board_size_var.get(), self.board_size_var.get(), self.get_mines(), load_main_menu)
            case "Liar":
                Liar(self.root, timer_enabled, self.board_size_var.get(), self.board_size_var.get(), self.get_mines(), load_main_menu)
            case "Two Tiles Away":
                TwoTilesAway(self.root, timer_enabled, self.board_size_var.get(), self.board_size_var.get(), self.get_mines(), load_main_menu)
            case "Vertical and Horizontal Clue":
                vnh_clue(self.root, timer_enabled, self.board_size_var.get(), self.board_size_var.get(), self.get_mines(), load_main_menu)
            
    def continue_game(self):
        self.main_frame.destroy()
        try:
            with open('game_state.json', 'r') as f:
                game_state = json.load(f)
                Minesweeper(self.root, enable_timer=game_state['enable_timer'], load_main_menu=load_main_menu).continue_game()
        except FileNotFoundError:
            messagebox.showerror("Minesweeper", "File not found.")
        except Exception as e:
            messagebox.showerror("Minesweeper", f"Failed to load game state: {e}")

    def quit_game(self):
        self.root.destroy()

def load_main_menu(root):
    main_menu = MainMenu(root)
