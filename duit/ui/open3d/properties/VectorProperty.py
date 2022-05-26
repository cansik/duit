from typing import Optional, Sequence, Dict

import vector
from open3d.cpu.pybind.visualization.gui import Widget
from open3d.visualization import gui

from duit.model.DataField import DataField
from duit.ui.annotations.VectorAnnotation import VectorAnnotation
from duit.ui.open3d.Open3dFieldProperty import Open3dFieldProperty


class VectorProperty(Open3dFieldProperty[VectorAnnotation]):
    def __init__(self, annotation: VectorAnnotation, model: Optional[DataField] = None):
        super().__init__(annotation, model)

    def create_field(self) -> Widget:
        vector_attributes = self._get_vector_attributes()
        attribute_widgets: Dict[str, gui.NumberEdit] = {}

        max_width = 230
        spacing = 15

        container = gui.Horiz(15)
        container.add_stretch()
        container.enabled = not self.annotation.read_only
        container.tooltip = self.annotation.tooltip

        def update_model():
            for attribute_name in vector_attributes:
                setattr(self.model.value, attribute_name, attribute_widgets[attribute_name].double_value)
            self.model.fire()

        for i, attribute_name in enumerate(vector_attributes):
            field = gui.NumberEdit(gui.NumberEdit.DOUBLE)
            field.decimal_precision = self.annotation.decimal_precision

            def on_ui_changed(value):
                update_model()

            field.set_on_value_changed(on_ui_changed)
            # container.add_child(gui.Label(f"{attribute_name}:"))
            field.set_preferred_width((max_width - ((len(vector_attributes) - 1) * spacing)) / len(vector_attributes))
            container.add_child(field)

            attribute_widgets[attribute_name] = field

        def on_dm_changed(value):
            for attribute_name in vector_attributes:
                attribute_widgets[attribute_name].double_value = getattr(value, attribute_name)

        self.model.on_changed.append(on_dm_changed)
        self.model.fire_latest()

        return container

    def _get_vector_attributes(self) -> Sequence[str]:
        value = self.model.value
        if isinstance(value, vector.Vector2D):
            return "x", "y"
        elif isinstance(value, vector.Vector3D):
            return "x", "y", "z"
        elif isinstance(value, vector.Vector4D):
            return "x", "y", "z", "t"
