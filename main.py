import tkinter as tk
from tkinter import messagebox
# from liar import Liar, LiarM
from minesweeper import Minesweeper, MainMenu
#minesweeper: Minesweeper, MainMenu
#liar: Liar, LiarM

if __name__ == "__main__":
    root = tk.Tk()
    main_menu = MainMenu(root)
    root.mainloop()
