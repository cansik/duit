from typing import Optional

from open3d.cpu.pybind.visualization.gui import Widget
from open3d.visualization import gui

from duit.model.DataField import DataField
from duit.ui.annotations import NumberAnnotation
from duit.ui.open3d.Open3dFieldProperty import Open3dFieldProperty


class NumberProperty(Open3dFieldProperty[NumberAnnotation]):
    def __init__(self, annotation: NumberAnnotation, model: Optional[DataField] = None):
        super().__init__(annotation, model)

    def create_field(self) -> Widget:
        edit_type = gui.NumberEdit.INT if isinstance(self.model.value, int) else gui.NumberEdit.DOUBLE
        field = gui.NumberEdit(edit_type)
        field.set_limits(self.annotation.limit_min, self.annotation.limit_max)
        field.enabled = not self.annotation.read_only or self.annotation.copy_content
        field.tooltip = self.annotation.tooltip
        field.decimal_precision = self.annotation.decimal_precision

        def on_dm_changed(value):
            field.set_value(value)

        def on_ui_changed(value):
            if self.annotation.read_only:
                field.text_value = self.model.value
            else:
                self.model.value = value

        self.model.on_changed.append(on_dm_changed)
        field.set_on_value_changed(on_ui_changed)

        self.model.fire_latest()
        return field
