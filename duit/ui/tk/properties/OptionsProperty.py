from typing import List, Any

import customtkinter as ctk
from customtkinter.windows.widgets.core_widget_classes import CTkBaseClass

from duit.model.DataField import DataField
from duit.ui.annotations.BooleanAnnotation import BooleanAnnotation
from duit.ui.tk.TkFieldProperty import TkFieldProperty


class OptionsProperty(TkFieldProperty[BooleanAnnotation, DataField]):
    def create_field(self, master) -> CTkBaseClass:
        option_var = ctk.StringVar(value="")

        field = ctk.CTkOptionMenu(master, variable=option_var)
        field.enabled = not self.annotation.read_only
        field.tooltip = self.annotation.tooltip

        str_options = [self.get_option_name(o) for o in self.options]

        field.configure(values=str_options)

        def on_dm_changed(value):
            option_var.set(self.get_option_name(value))

        def on_ui_changed(value):
            self.model.value = self.options[str_options.index(value)]

        self.model.on_changed.append(on_dm_changed)
        field.configure(command=on_ui_changed)

        self.model.fire_latest()
        return field

    @property
    def options(self) -> List[Any]:
        return self.annotation.options

    def get_option_name(self, option) -> str:
        return str(option)
