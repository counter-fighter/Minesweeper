import tkinter as tk
from tkinter import messagebox
from minesweeper import MainMenu
from minesweeper import Minesweeper

if __name__ == "__main__":
    root = tk.Tk()
    root.minsize(500, 500)
    main_menu = MainMenu(root)
    root.mainloop()
