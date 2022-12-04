import tkinter as tk

import customtkinter as ctk
from customtkinter.windows.widgets.core_widget_classes import CTkBaseClass

from duit.ui.annotations.SliderAnnotation import SliderAnnotation
from duit.ui.tk.TkFieldProperty import TkFieldProperty


class SliderProperty(TkFieldProperty[SliderAnnotation]):
    def create_field(self, master) -> CTkBaseClass:
        int_variable = ctk.IntVar()
        field = ctk.CTkSlider(master, variable=int_variable,
                              from_=self.annotation.limit_min,
                              to=self.annotation.limit_max)

        def on_dm_changed(value):
            int_variable.set(value)

        def on_ui_changed(event):
            self.model.value = int_variable.get()

        self.model.on_changed.append(on_dm_changed)
        field.configure(command=on_ui_changed)

        self.model.fire_latest()

        return field
