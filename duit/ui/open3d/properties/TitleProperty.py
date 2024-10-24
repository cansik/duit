from typing import Optional, Sequence

from open3d.cpu.pybind.visualization.gui import Widget
from open3d.visualization import gui

from duit.model.DataField import DataField
from duit.ui.annotations.TitleAnnoation import TitleAnnotation
from duit.ui.open3d import Open3dContext
from duit.ui.open3d.Open3dFieldProperty import Open3dFieldProperty


class TitleProperty(Open3dFieldProperty[TitleAnnotation, DataField]):
    def __init__(self, annotation: TitleAnnotation, model: Optional[DataField] = None):
        """
        Initializes a TitleProperty instance.

        Args:
            annotation (TitleAnnotation): The TextAnnotation associated with this property.
            model (Optional[DataField]): The data model field to bind this property to.
        """
        super().__init__(annotation, model, raw_output=True)

    def create_field(self) -> Sequence[Widget]:
        """
        Creates a GUI widget for the text property.

        Returns:
            Widget: The created GUI widget for the text property.
        """
        field = gui.Label(self.model.value)
        field.enabled = not self.annotation.read_only
        field.tooltip = self.annotation.tooltip

        field.font_id = Open3dContext.OPEN3D_TITLE_FONT_ID

        text_color = self.annotation.text_color

        if self.annotation.text_color is not None:
            field.text_color = gui.Color(r=text_color[0] / 255, g=text_color[1] / 255, b=text_color[2] / 255)

        def on_dm_changed(value):
            field.text = value

        self.model.on_changed.append(on_dm_changed)
        self.model.fire_latest()

        spacer = gui.Horiz()
        return spacer, spacer, field, gui.Label("")
