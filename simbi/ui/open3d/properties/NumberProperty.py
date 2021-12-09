from typing import Optional

from open3d.cpu.pybind.visualization.gui import Widget
from open3d.visualization import gui

from simbi.model.DataField import DataField
from simbi.ui.annotations import NumberAnnotation
from simbi.ui.open3d.Open3dFieldProperty import Open3dFieldProperty


class NumberProperty(Open3dFieldProperty[NumberAnnotation]):
    def __init__(self, annotation: NumberAnnotation, model: Optional[DataField] = None):
        super().__init__(annotation, model)

    def create_field(self) -> Widget:
        edit_type = gui.NumberEdit.INT if isinstance(self.model.value, int) else gui.NumberEdit.DOUBLE
        field = gui.NumberEdit(edit_type)
        field.set_limits(self.annotation.limit_min, self.annotation.limit_max)

        def on_dm_changed(value):
            field.set_value(value)

        def on_ui_changed(value):
            self.model.value = value

        self.model.on_changed.append(on_dm_changed)
        field.set_on_value_changed(on_ui_changed)

        self.model.fire_latest()
        return field
