from customtkinter import CTkProgressBar
from customtkinter.windows.widgets.core_widget_classes import CTkBaseClass

from duit.model.DataField import DataField
from duit.ui.annotations.ProgressAnnotation import ProgressAnnotation
from duit.ui.tk.TkFieldProperty import TkFieldProperty


class ProgressProperty(TkFieldProperty[ProgressAnnotation, DataField]):
    def create_field(self, master) -> CTkBaseClass:
        """
        Creates a progress bar for the DataField.

        Args:
            master: The parent widget.

        Returns:
            CTkBaseClass: The created progress bar.
        """
        field = CTkProgressBar(master)
        field.readonly = self.annotation.read_only

        def on_dm_changed(value):
            field.set(value)

        self.model.on_changed.append(on_dm_changed)

        self.model.fire_latest()
        return field
