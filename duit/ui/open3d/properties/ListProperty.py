from typing import Optional, Any, List

from open3d.cpu.pybind.visualization.gui import Widget
from open3d.visualization import gui

from duit.model.SelectableDataList import SelectableDataList
from duit.ui.annotations.ListAnnotation import ListAnnotation
from duit.ui.open3d.Open3dFieldProperty import Open3dFieldProperty


class ListProperty(Open3dFieldProperty[ListAnnotation, SelectableDataList]):
    """
    Property class for handling ListAnnotation.

    This property generates a combobox or selection box widget for selecting from a list of options.

    """

    def __init__(self, annotation: ListAnnotation, model: Optional[SelectableDataList] = None):
        """
        Initialize a ListProperty.

        :param annotation: The ListAnnotation associated with this property.
        :param model: The data model for this property (default is None).
        """
        super().__init__(annotation, model)

    def create_field(self) -> Widget:
        """
        Create the field widget for the ListProperty.

        This method generates a combobox or selection box widget based on the platform, for selecting options from a list.

        :return: The combobox or selection box widget.
        """
        field = gui.Combobox()
        field.enabled = not self.annotation.read_only
        field.tooltip = self.annotation.tooltip

        def on_dm_changed(value):
            field.clear_items()

            for option in self.options:
                field.add_item(self.get_option_name(option))

        def on_dm_selection_changed(index):
            if index is not None:
                field.selected_index = index

        def on_ui_selection_changed(value, index):
            self.model.selected_index = index

        self.model.on_changed += on_dm_changed
        self.model.on_index_changed += on_dm_selection_changed
        field.set_on_selection_changed(on_ui_selection_changed)

        self.model.fire_latest()
        self.model.on_index_changed.invoke_latest(self.model.selected_index)
        return field

    @property
    def options(self) -> List[Any]:
        """
        Get the list of available options.

        :return: A list of available options.
        """
        return self.model.value

    def get_option_name(self, option) -> str:
        """
        Get the name of an option.

        :param option: The option for which to retrieve the name.
        :return: The name of the option.
        """
        return str(option)
