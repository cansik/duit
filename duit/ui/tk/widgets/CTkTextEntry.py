import customtkinter
from customtkinter import CTkEntry


class CTkTextEntry(CTkEntry):
    def __init__(self, master: any, **kwargs):
        super().__init__(master, **kwargs)
        self._variable = customtkinter.StringVar()
        self.configure(textvariable=self._variable)
        self._readonly = False

    @property
    def readonly(self) -> bool:
        return self._readonly

    @readonly.setter
    def readonly(self, value: bool):
        self._readonly = value
        if value:
            self.configure(state="readonly")
        else:
            self.configure(state="normal")

    @property
    def text(self) -> str:
        return self._variable.get()

    @text.setter
    def text(self, text: str):
        self._variable.set(text)

    def on_changed(self, callback):
        self.bind("<FocusOut>", callback)
