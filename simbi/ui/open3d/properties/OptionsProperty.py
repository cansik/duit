from functools import partial
from typing import Optional

from open3d.cpu.pybind.visualization.gui import Widget
from open3d.visualization import gui

from simbi.model.DataModel import DataModel
from simbi.ui.annotations.OptionsAnnotation import OptionsAnnotation
from simbi.ui.open3d.Open3dFieldProperty import Open3dFieldProperty


class OptionsProperty(Open3dFieldProperty[OptionsAnnotation]):
    def __init__(self, annotation: OptionsAnnotation, model: Optional[DataModel] = None):
        super().__init__(annotation, model)

    def create_field(self) -> Widget:
        field = gui.Combobox()

        for option in self.annotation.options:
            field.add_item(str(option))

        def on_dm_changed(value, f: gui.NumberEdit):
            f.selected_index = self.annotation.options.index(value)

        def on_ui_changed(value, index, m: DataModel):
            m.value = self.annotation.options[index]

        self.model.on_changed.append(partial(on_dm_changed, f=field))
        field.set_on_selection_changed(partial(on_ui_changed, m=self.model))

        self.model.fire_latest()
        return field
