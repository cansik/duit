from open3d.visualization import gui

from simbi.ui.PropertyRegistry import UI_PROPERTY_REGISTRY
from simbi.ui.annotations import find_all_ui_annotations


class PropertyPanel(gui.Vert):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.em = 15

        self._data_context = None
        self._grid = gui.VGrid(2, 0.25 * self.em)
        self.add_child(self._grid)

    @property
    def data_context(self):
        return self._data_context

    @data_context.setter
    def data_context(self, value):
        self._data_context = value
        self._create_properties()

    def _create_properties(self):
        # todo: remove children

        if self._data_context is None:
            return

        annotations = find_all_ui_annotations(self._data_context)
        for var_name, (model, anns) in annotations.items():
            for ann in anns:
                property_field = UI_PROPERTY_REGISTRY[type(ann)](ann, model)
                widgets = property_field.create_widgets()

                for widget in widgets:
                    self._grid.add_child(widget)



