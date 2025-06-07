import tkinter as tk
from calc import Calculator

if __name__ == "__main__":
    root = tk.Tk()
    calc = Calculator(root)
    root.mainloop()