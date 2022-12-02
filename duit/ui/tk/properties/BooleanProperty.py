import customtkinter as ctk
from customtkinter.widgets.widget_base_class import CTkBaseClass

from duit.ui.annotations.BooleanAnnotation import BooleanAnnotation
from duit.ui.tk.TkFieldProperty import TkFieldProperty


class BooleanProperty(TkFieldProperty[BooleanAnnotation]):
    def create_field(self, master) -> CTkBaseClass:
        field = ctk.CTkCheckBox(master, text="")
        field.tooltip = self.annotation.tooltip
        field.enabled = not self.annotation.read_only

        def on_dm_changed(value):
            field.check_state = self.model.value

        def on_ui_changed():
            self.model.value = field.check_state

        self.model.on_changed.append(on_dm_changed)
        field.function = on_ui_changed

        self.model.fire_latest()
        field.draw()

        return field
