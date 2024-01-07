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

    app = ctk.CTk()
    app.title("Configuration")
    app.geometry("400x600")

    panel = TkPropertyPanel(app)
    panel.pack(fill=tk.BOTH, expand=True)

    panel.data_context = config

    def on_hungry(value):
        print(f"hungry changed to: {value}")

    def on_resolution_changed(value):
        print(f"Resolution: {value}")

    config.hungry.on_changed += on_hungry
    config.resolution.on_changed += on_resolution_changed

    app.mainloop()


if __name__ == '__main__':
    main()
