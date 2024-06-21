import tkinter as tk
from tkinter import messagebox
from liar import Liar, LiarM
#minesweeper: Minesweeper, MainMenu
#liar: Liar, LiarM

if __name__ == "__main__":
    root = tk.Tk()
    root.minsize(500, 500)
    main_menu = LiarM(root)
    root.mainloop()
