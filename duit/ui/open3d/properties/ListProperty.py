import sys
from typing import Optional, Any, List

from open3d.cpu.pybind.visualization.gui import Widget
from open3d.visualization import gui

from duit.model.SelectableDataList import SelectableDataList
from duit.ui.annotations.ListAnnotation import ListAnnotation
from duit.ui.open3d.Open3dFieldProperty import Open3dFieldProperty
from duit.ui.open3d.widgets.SelectionBox import SelectionBox


class ListProperty(Open3dFieldProperty[ListAnnotation, SelectableDataList]):
    def __init__(self, annotation: ListAnnotation, model: Optional[SelectableDataList] = None):
        super().__init__(annotation, model)

    def create_field(self) -> Widget:
        # workaround for issue https://github.com/isl-org/Open3D/issues/6024
        if sys.platform == "darwin":
            field = SelectionBox()
        else:
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
        return self.model.value

    def get_option_name(self, option) -> str:
        return str(option)
