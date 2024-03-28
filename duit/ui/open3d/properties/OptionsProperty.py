from typing import Optional, Any, List

from open3d.cpu.pybind.visualization.gui import Widget
from open3d.visualization import gui

from duit.model.DataField import DataField
from duit.ui.annotations.OptionsAnnotation import OptionsAnnotation
from duit.ui.open3d.Open3dFieldProperty import Open3dFieldProperty


class OptionsProperty(Open3dFieldProperty[OptionsAnnotation, DataField]):
    """
    Property class for handling OptionsAnnotation.

    This property generates a selection box or combobox for selecting from a list of options.

    """

    def __init__(self, annotation: OptionsAnnotation, model: Optional[DataField] = None):
        """
        Initialize an OptionsProperty.

        :param annotation: The OptionsAnnotation associated with this property.
        :param model: The data model for this property (default is None).
        """
        super().__init__(annotation, model)

    def create_field(self) -> Widget:
        """
        Create the field widget for the OptionsProperty.

        This method generates a selection box or combobox for selecting from a list of options.

        :return: The selection box or combobox widget.
        """
        field = gui.Combobox()
        field.enabled = not self.annotation.read_only
        field.tooltip = self.annotation.tooltip

        for option in self.options:
            field.add_item(self.get_option_name(option))

        def on_dm_changed(value):
            field.selected_index = self.options.index(value)

        def on_ui_changed(value, index):
            self.model.value = self.options[index]

        self.model.on_changed.append(on_dm_changed)
        field.set_on_selection_changed(on_ui_changed)

        self.model.fire_latest()
        return field

    @property
    def options(self) -> List[Any]:
        return self.annotation.options

    def get_option_name(self, option) -> str:
        return str(option)
