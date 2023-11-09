from typing import Optional, Dict

from open3d.cpu.pybind.visualization.gui import Widget
from open3d.visualization import gui

from duit.model.DataField import DataField
from duit.ui.annotations.VectorAnnotation import VectorAnnotation
from duit.ui.open3d import Open3dContext
from duit.ui.open3d.Open3dFieldProperty import Open3dFieldProperty
from duit.utils import _vector


class VectorProperty(Open3dFieldProperty[VectorAnnotation, DataField]):
    def __init__(self, annotation: VectorAnnotation, model: Optional[DataField] = None):
        """
        Initializes a VectorProperty instance.

        Args:
            annotation (VectorAnnotation): The VectorAnnotation associated with this property.
            model (Optional[DataField]): The data model field to bind this property to.
        """
        super().__init__(annotation, model)

    def create_field(self) -> Widget:
        """
        Creates a GUI widget for the vector property.

        Returns:
            Widget: The created GUI widget for the vector property.
        """
        vector_attributes = _vector.get_vector_attributes(self.model.value)
        attribute_widgets: Dict[str, gui.NumberEdit] = {}

        container = gui.Horiz(self.annotation.spacing * Open3dContext.OPEN3D_FONT_EM)

        labels = vector_attributes
        if self.annotation.labels is not None:
            assert len(labels) == len(self.annotation.labels), f"Label count is not correct for {self.annotation.name}!"
            labels = self.annotation.labels

        def update_model():
            for attribute_name in vector_attributes:
                setattr(self.model.value, attribute_name, attribute_widgets[attribute_name].double_value)
            self.model.fire()

        def update_ui():
            value = self.model.value
            for attribute_name in vector_attributes:
                attribute_widgets[attribute_name].double_value = getattr(value, attribute_name)

        for i, attribute_name in enumerate(vector_attributes):
            field = gui.NumberEdit(gui.NumberEdit.DOUBLE)
            field.decimal_precision = self.annotation.decimal_precision

            field.enabled = not self.annotation.read_only or self.annotation.copy_content
            field.tooltip = self.annotation.tooltip

            def on_ui_changed(value):
                if self.annotation.read_only:
                    update_ui()
                else:
                    update_model()

            field.set_on_value_changed(on_ui_changed)
            field.set_preferred_width(self.annotation.max_width * Open3dContext.OPEN3D_FONT_EM)

            label = labels[i]

            if self.annotation.hide_labels:
                field.tooltip = f"{label}"
            else:
                container.add_child(gui.Label(f"{label}:"))
            container.add_child(field)

            attribute_widgets[attribute_name] = field
        container.add_stretch()

        def on_dm_changed(value):
            update_ui()

        self.model.on_changed.append(on_dm_changed)
        self.model.fire_latest()

        return container
