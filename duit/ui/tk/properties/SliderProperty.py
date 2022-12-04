import tkinter as tk

import customtkinter as ctk
from customtkinter.windows.widgets.core_widget_classes import CTkBaseClass

from duit.ui.annotations.SliderAnnotation import SliderAnnotation
from duit.ui.tk.TkFieldProperty import TkFieldProperty
from duit.ui.tk.widgets.CTkNumberEntry import CTkNumberEntry


class SliderProperty(TkFieldProperty[SliderAnnotation]):
    def create_field(self, master) -> CTkBaseClass:
        frame = ctk.CTkFrame(master)

        data_variable = ctk.IntVar() if isinstance(self.model.value, int) else ctk.DoubleVar()
        field = ctk.CTkSlider(frame,
                              variable=data_variable,
                              from_=self.annotation.limit_min,
                              to=self.annotation.limit_max,
                              width=140
                              )
        field.grid(row=0, column=0, padx=5, pady=0)

        number_entry = CTkNumberEntry(frame,
                                      self.model.value,
                                      self.annotation.limit_min,
                                      self.annotation.limit_max,
                                      width=80)
        number_entry.grid(row=0, column=1, padx=5, pady=0)

        def on_dm_changed(value):
            data_variable.set(value)
            number_entry.value = value

        def on_ui_changed(event):
            self.model.value = data_variable.get()

        def on_entry_changed(event):
            self.model.value = number_entry.value

        self.model.on_changed.append(on_dm_changed)
        field.configure(command=on_ui_changed)
        number_entry.on_changed(on_entry_changed)

        self.model.fire_latest()

        return frame
