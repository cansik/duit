import tkinter as tk
from tkinter import ttk

from customtkinter import CTkFrame, CTkLabel


class CTkCollapsable(CTkFrame):

    def __init__(self, master, title="", *args, **options):
        CTkFrame.__init__(self, master, *args, **options)

        self.show = tk.BooleanVar()
        self.show.set(False)

        self.title_frame = CTkFrame(self)
        self.title_frame.pack(fill="x", expand=1)

        self.label = CTkLabel(self.title_frame, text=title)
        self.label.pack(side="left", fill="x", expand=1)

        self.toggle_button = ttk.Checkbutton(self.title_frame, width=2, text="▶", command=self.toggle,
                                             variable=self.show, style="Toolbutton")
        self.toggle_button.pack(side="left")

        self.sub_frame = CTkFrame(self)

    def toggle(self):
        if bool(self.show.get()):
            self.sub_frame.pack(fill="x", expand=1)
            self.toggle_button.configure(text="▼")
        else:
            self.sub_frame.forget()
            self.toggle_button.configure(text="▶")
