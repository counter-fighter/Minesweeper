import tkinter as tk
from tkinter import messagebox
from main_menu import load_main_menu

if __name__ == "__main__":
    root = tk.Tk()
    load_main_menu(root)
    root.mainloop()
