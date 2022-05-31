from customtkinter.widgets.widget_base_class import CTkBaseClass

from duit.ui.annotations import NumberAnnotation
from duit.ui.tk.TkFieldProperty import TkFieldProperty
import customtkinter as ctk
import tkinter as tk


class NumberProperty(TkFieldProperty[NumberAnnotation]):
    def create_field(self, master) -> CTkBaseClass:
        field = ctk.CTkEntry(master)
        data_type = int if isinstance(self.model.value, int) else float

        def on_dm_changed(value):
            str_value = f"{value:.2f}" if data_type is float else f"{round(value)}"

            field.delete(0, tk.END)
            field.insert(0, str_value)

        def on_ui_changed(event):
            self.model.value = float(field.get()) if data_type is float else int(field.get())

        self.model.on_changed.append(on_dm_changed)
        field.bind("<FocusOut>", on_ui_changed)

        self.model.fire_latest()

        return field
