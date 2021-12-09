from functools import partial
from typing import Optional

from open3d.cpu.pybind.visualization.gui import Widget
from open3d.visualization import gui

from simbi.model.DataModel import DataModel
from simbi.ui.annotations import NumberAnnotation
from simbi.ui.open3d.Open3dFieldProperty import Open3dFieldProperty


class NumberProperty(Open3dFieldProperty):
    def __init__(self, annotation: NumberAnnotation, model: Optional[DataModel] = None):
        super().__init__(annotation, model)

    def create_field(self) -> Widget:
        edit_type = gui.NumberEdit.INT if isinstance(self.model.value, int) else gui.NumberEdit.DOUBLE
        field = gui.NumberEdit(edit_type)
        field.set_limits(self.annotation.limit_min, self.annotation.limit_max)

        def on_dm_changed(value, f: gui.NumberEdit):
            f.set_value(value)

        def on_ui_changed(value, m: DataModel):
            m.value = value

        self.model.on_changed.append(partial(on_dm_changed, f=field))
        field.set_on_value_changed(partial(on_ui_changed, m=self.model))

        self.model.fire_latest()
        return field
