import logging

from open3d.visualization import gui
from open3d.visualization.gui import Widget

from simbi.collections.Stack import Stack
from simbi.ui.PropertyRegistry import UI_PROPERTY_REGISTRY
from simbi.ui.annotations import find_all_ui_annotations
from simbi.ui.annotations.container.EndSectionAnnotation import EndSectionAnnotation
from simbi.ui.annotations.container.StartSectionAnnotation import StartSectionAnnotation


class PropertyPanel(gui.Vert):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.em = 15

        self._data_context = None
        self._containers: Stack[Widget] = Stack()

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

        # todo: refactor this ugly method
        annotations = find_all_ui_annotations(self._data_context)
        for var_name, (model, anns) in annotations.items():
            pop_after = False

            for ann in anns:
                ann_type = type(ann)

                # check for container
                if isinstance(ann, StartSectionAnnotation):
                    settings = gui.CollapsableVert(ann.name, 0.25 * self.em, gui.Margins(self.em, 0, 0, 0))
                    settings.set_is_open(not ann.collapsed)
                    grid = gui.VGrid(2, 0.25 * self.em)
                    settings.add_child(grid)
                    self.add_child(settings)
                    self._containers.push(grid)
                    continue

                if isinstance(ann, EndSectionAnnotation):
                    pop_after = True
                    continue

                if ann_type not in UI_PROPERTY_REGISTRY:
                    logging.warning(f"Annotation not registered: {ann_type.__name__}")
                    continue

                # add property
                property_field = UI_PROPERTY_REGISTRY[ann_type](ann, model)
                widgets = property_field.create_widgets()

                for widget in widgets:
                    self._current_container.add_child(widget)

            if pop_after:
                self._containers.pop()

        # add all containers that are left
        while not self._containers.is_empty:
            self.add_child(self._containers.pop())

    @property
    def _current_container(self):
        if self._containers.is_empty:
            self._containers.push(gui.VGrid(2, 0.25 * self.em))

        return self._containers.peek()
