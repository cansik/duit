from customtkinter.widgets.widget_base_class import CTkBaseClass

from duit.ui.annotations import NumberAnnotation
from duit.ui.tk.TkFieldProperty import TkFieldProperty
import customtkinter as ctk
import tkinter as tk


class NumberProperty(TkFieldProperty[NumberAnnotation]):
    def create_field(self, master) -> CTkBaseClass:
        field = ctk.CTkEntry(master)

        def set_text(text: str):
            field.delete(0, tk.END)
            field.insert(0, text)

        def on_dm_changed(value):
            set_text(self.get_value_str())

        def on_ui_changed(event):
            self.convert_to_value(field)

        self.model.on_changed.append(on_dm_changed)
        field.bind("<FocusOut>", on_ui_changed)

        self.model.fire_latest()

        return field

    def get_value_str(self) -> str:
        if isinstance(self.model.value, int):
            return f"{self.model.value}"
        else:
            return f"{round(self.model.value, self.annotation.decimal_precision)}"

    def convert_to_value(self, field: ctk.CTkEntry):
        content = field.get()

        if not self.is_number(content):
            self.model.fire()
            return

        value = float(content)
        value = max(self.annotation.limit_min, value)
        value = min(self.annotation.limit_max, value)

        if isinstance(self.model.value, int):
            value = int(value)
        else:
            value = float(value)

        self.model.value = value

    @staticmethod
    def is_number(value: str):
        try:
            float(value)
            return True
        except ValueError:
            return False
