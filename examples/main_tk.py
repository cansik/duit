import tkinter as tk
import customtkinter as ctk

from Config import Config
from duit.ui.tk.TkPropertyPanel import TkPropertyPanel
from duit.ui.tk.TkPropertyRegistry import init_tk_registry


def main():
    init_tk_registry()

    config = Config()

    ctk.set_appearance_mode("dark")  # Modes: system (default), light, dark
    ctk.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green

    app = ctk.CTk()  # create CTk window like you do with the Tk window
    app.title("Configuration")
    app.geometry("400x600")

    panel = TkPropertyPanel(app)
    panel.pack(fill=tk.BOTH, expand=True)

    panel.data_context = config

    app.mainloop()


if __name__ == '__main__':
    main()
