import tkinter

import customtkinter as ctk
from customtkinter.windows.widgets.core_widget_classes import CTkBaseClass

from duit.model.DataField import DataField
from duit.ui.annotations.BooleanAnnotation import BooleanAnnotation
from duit.ui.tk.TkFieldProperty import TkFieldProperty


class BooleanProperty(TkFieldProperty[BooleanAnnotation, DataField]):
    def create_field(self, master) -> CTkBaseClass:
        """
        Create and return the GUI field for the boolean property.

        Args:
            master: The master widget where the field will be created.

        Returns:
            CTkBaseClass: The created GUI field.
        """
        check_var = tkinter.BooleanVar()

        field = ctk.CTkSwitch(master, text="", variable=check_var)
        field.tooltip = self.annotation.tooltip
        field.enabled = not self.annotation.read_only

        def on_dm_changed(value):
            check_var.set(self.model.value)

        def on_ui_changed():
            self.model.value = check_var.get()

        self.model.on_changed.append(on_dm_changed)
        field.configure(command=on_ui_changed)

        self.model.fire_latest()
        return field
