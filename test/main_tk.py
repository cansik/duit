import tkinter as tk
from tkinter import Menu

import customtkinter as ctk
from Config import Config
from duit.ui.tk.TkPropertyPanel import TkPropertyPanel
from duit.ui.tk.TkPropertyRegistry import init_tk_registry


def main():
    init_tk_registry()

    config = Config()

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    app = ctk.CTk()
    app.title("Configuration")
    app.geometry("400x600")

    # Create a menu bar
    menubar = Menu(app)
    app.config(menu=menubar)

    # Create a File menu
    file_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="File", menu=file_menu)

    # Add an exit command to the File menu
    def exit_app():
        app.destroy()

    file_menu.add_command(label="Exit", command=exit_app)

    panel = TkPropertyPanel(app)
    panel.pack(fill=tk.BOTH, expand=True)
    panel.data_context = config

    def on_hungry(value):
        print(f"hungry changed to: {value}")

    config.hungry.on_changed += on_hungry

    app.mainloop()


if __name__ == '__main__':
    main()
