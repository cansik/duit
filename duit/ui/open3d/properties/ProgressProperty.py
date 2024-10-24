from typing import Optional

from open3d.cpu.pybind.visualization.gui import Widget
from open3d.visualization import gui

from duit.model.DataField import DataField
from duit.ui.annotations.ProgressAnnotation import ProgressAnnotation
from duit.ui.open3d import Open3dContext
from duit.ui.open3d.Open3dFieldProperty import Open3dFieldProperty


class ProgressProperty(Open3dFieldProperty[ProgressAnnotation, DataField]):
    """A property that renders a progress bar for a DataField."""

    def __init__(self, annotation: ProgressAnnotation, model: Optional[DataField] = None):
        super().__init__(annotation, model)

    def create_field(self) -> Widget:
        """Creates a progress bar for the DataField."""

        field = gui.ProgressBar()
        field.tooltip = self.annotation.tooltip

        def on_dm_changed(value):
            field.value = value

        self.model.on_changed.append(on_dm_changed)
        self.model.fire_latest()

        container = gui.Horiz()
        container.add_child(field)
        container.preferred_height = int(Open3dContext.OPEN3D_FONT_EM * 1.2)
        return container
