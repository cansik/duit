from customtkinter.windows.widgets.core_widget_classes import CTkBaseClass

from duit.model.DataField import DataField
from duit.ui.annotations.TextAnnotation import TextAnnotation
from duit.ui.tk.TkFieldProperty import TkFieldProperty
from duit.ui.tk.widgets.CTkTextEntry import CTkTextEntry


class TextProperty(TkFieldProperty[TextAnnotation, DataField]):
    def create_field(self, master) -> CTkBaseClass:
        """
        Create a text entry field for the given text annotation.

        Args:
            master: The parent widget.

        Returns:
            CTkBaseClass: The created text entry field.
        """
        field = CTkTextEntry(master, placeholder_text=self.annotation.placeholder_text)
        field.readonly = self.annotation.read_only

        def on_dm_changed(value):
            field.text = value

        def on_ui_changed(event):
            self.model.value = field.text

        self.model.on_changed.append(on_dm_changed)
        field.on_changed(on_ui_changed)

        self.model.fire_latest()
        return field
