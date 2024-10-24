from typing import Optional

from open3d.cpu.pybind.visualization.gui import Widget
from open3d.visualization import gui

from duit.model.DataField import DataField
from duit.ui.annotations.TextAnnotation import TextAnnotation
from duit.ui.open3d.Open3dFieldProperty import Open3dFieldProperty
from duit.ui.open3d.widgets.CopyToClipboardButton import CopyToClipboardButton


class TextProperty(Open3dFieldProperty[TextAnnotation, DataField]):
    def __init__(self, annotation: TextAnnotation, model: Optional[DataField] = None):
        """
        Initializes a TextProperty instance.

        Args:
            annotation (TextAnnotation): The TextAnnotation associated with this property.
            model (Optional[DataField]): The data model field to bind this property to.
        """
        super().__init__(annotation, model)

    def create_field(self) -> Widget:
        """
        Creates a GUI widget for the text property.

        Returns:
            Widget: The created GUI widget for the text property.
        """
        field = gui.TextEdit()
        field.placeholder_text = self.annotation.placeholder_text
        field.enabled = not self.annotation.read_only
        field.tooltip = self.annotation.tooltip

        def on_dm_changed(value):
            field.text_value = value

        def on_ui_changed(value):
            if self.annotation.read_only:
                field.text_value = self.model.value
            else:
                self.model.value = value

        self.model.on_changed.append(on_dm_changed)
        field.set_on_value_changed(on_ui_changed)

        self.model.fire_latest()

        if self.annotation.read_only and self.annotation.copy_content:
            container = gui.Horiz(4)
            container.add_child(field)
            container.add_child(CopyToClipboardButton(self.model))
            return container

        return field
