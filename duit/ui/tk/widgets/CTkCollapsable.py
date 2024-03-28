import tkinter as tk
from tkinter import ttk

from customtkinter import CTkFrame, CTkLabel


class CTkCollapsable(CTkFrame):

    def __init__(self, master, text="", shown: bool = True, *args, **options):
        CTkFrame.__init__(self, master, *args, **options)

        self.show = tk.BooleanVar()
        self.show.set(shown)

        self.title_frame = CTkFrame(self)
        self.title_frame.pack(fill="x", expand=1)

        self.toggle_button = ttk.Checkbutton(self.title_frame, width=2, text="▶", command=self.toggle,
                                             variable=self.show, style="Toolbutton")
        self.toggle_button.pack(side="left")

        self.label = CTkLabel(self.title_frame, text=text)
        self.label.pack(side="left", fill="x", expand=1)

        self.frame = CTkFrame(self)
        self.frame.configure(fg_color="gray16")

        self.toggle()

    def toggle(self):
        if self.show.get():
            self.frame.pack(fill="x", expand=1)
            self.toggle_button.configure(text="▼")
        else:
            self.frame.forget()
            self.toggle_button.configure(text="▶")
