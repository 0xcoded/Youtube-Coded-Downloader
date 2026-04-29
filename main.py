import tkinter as tk
import gui
import downloader


if __name__ == "__main__":
    tk.messagebox.showinfo(title="Bienvenido", message="Collaboradores:\n0xcoded\nHanco89")
    root = tk.Tk()
    app = gui.Gui(root)
    root.mainloop()