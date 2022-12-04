import tkinter as tk
from customtkinter import CTkEntry


class CTkTextEntry(CTkEntry):

    @property
    def text(self) -> str:
        return self.get()

    @text.setter
    def text(self, text: str):
        self.delete(0, tk.END)
        self.insert(0, text)

    def on_changed(self, callback):
        self.bind("<FocusOut>", callback)
