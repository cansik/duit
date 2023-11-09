from typing import Optional

from open3d.cpu.pybind.visualization.gui import Widget
from open3d.visualization import gui

from duit.model.DataField import DataField
from duit.ui.annotations.SliderAnnotation import SliderAnnotation
from duit.ui.open3d.Open3dFieldProperty import Open3dFieldProperty


class SliderProperty(Open3dFieldProperty[SliderAnnotation, DataField]):
    def __init__(self, annotation: SliderAnnotation, model: Optional[DataField] = None):
        """
        Initializes a SliderProperty instance.

        Args:
            annotation (SliderAnnotation): The SliderAnnotation associated with this property.
            model (Optional[DataField]): The data model field to bind this property to.
        """
        super().__init__(annotation, model)

    def create_field(self) -> Widget:
        """
        Creates a GUI widget for the slider property.

        Returns:
            Widget: The created GUI widget for the slider property.
        """
        slider_type = gui.Slider.INT if isinstance(self.model.value, int) else gui.Slider.DOUBLE
        field = gui.Slider(slider_type)
        field.set_limits(self.annotation.limit_min, self.annotation.limit_max)
        field.enabled = not self.annotation.read_only
        field.tooltip = self.annotation.tooltip

        number_type = gui.NumberEdit.INT if isinstance(self.model.value, int) else gui.NumberEdit.DOUBLE
        number_field = gui.NumberEdit(number_type)
        number_field.set_limits(self.annotation.limit_min, self.annotation.limit_max)
        number_field.enabled = not self.annotation.read_only
        number_field.tooltip = self.annotation.tooltip

        def on_dm_changed(value):
            if slider_type == gui.Slider.INT:
                field.int_value = int(round(value))
                number_field.int_value = int(round(value))
            else:
                field.double_value = value
                number_field.double_value = value

        def on_number_ui_changed(value):
            self.model.value = value

        def on_ui_changed(value):
            if slider_type == gui.Slider.INT:
                self.model.value = int(round(value))
            else:
                self.model.value = value

        self.model.on_changed.append(on_dm_changed)
        field.set_on_value_changed(on_ui_changed)
        number_field.set_on_value_changed(on_number_ui_changed)

        self.model.fire_latest()

        if not self.annotation.show_number_field:
            return field

        container = gui.Horiz(4)
        container.add_child(field)
        container.add_child(number_field)
        return container
