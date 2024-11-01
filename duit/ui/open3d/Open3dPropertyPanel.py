import logging
from typing import Any

from open3d.visualization import gui

from duit.collections.Stack import Stack
from duit.ui.PropertyRegistry import UI_PROPERTY_REGISTRY
from duit.ui.annotations import find_all_ui_annotations
from duit.ui.annotations.container.EndSectionAnnotation import EndSectionAnnotation
from duit.ui.annotations.container.StartSectionAnnotation import StartSectionAnnotation
from duit.ui.annotations.container.SubSectionAnnotation import SubSectionAnnotation
from duit.ui.open3d import Open3dContext


class Open3dPropertyPanel(gui.WidgetProxy):
    def __init__(self, window: gui.Window):
        """
        Initialize an Open3dPropertyPanel.

        :param window: The Open3D window.
        """
        gui.WidgetProxy.__init__(self)

        self.window = window
        self.em = self.window.theme.font_size

        # set global font em to be used in widgets
        Open3dContext.OPEN3D_FONT_EM = self.em
        Open3dContext.OPEN3D_MAIN_WINDOW = self.window

        # currently does not work on windows
        # title_font = gui.FontDescription(typeface=gui.FontDescription.SANS_SERIF,
        #                                  style=gui.FontStyle.BOLD)
        # title_font_id = gui.Application.instance.add_font(title_font)
        # Open3dContext.OPEN3D_TITLE_FONT_ID = title_font_id

        self.widget: gui.Vert = gui.Vert()
        self.container_margins = gui.Margins(self.em, 0.25 * self.em, self.em, 0.25 * self.em)
        self.container_spacing = 0.25 * self.em
        self._data_context = None

        self.max_stack_depth = 5
        self.stack_depth = 0

    @property
    def data_context(self):
        return self._data_context

    @data_context.setter
    def data_context(self, value):
        self._data_context = value
        self._create_panel()

    def _create_panel(self):
        self.widget = gui.Vert()

        if self._data_context is None:
            return

        self._create_properties(self.data_context, self.widget)
        self.set_widget(self.widget)

    def __on_recreate_requested(self, *args):
        self._create_panel()

    def _create_properties(self, obj: Any, root_widget: gui.Widget):
        self.stack_depth += 1

        containers: Stack[gui.Widget] = Stack()
        containers.push(gui.VGrid(2, self.container_spacing, self.container_margins))

        annotations = find_all_ui_annotations(obj)
        for var_name, (model, anns) in annotations.items():
            pop_after = False

            anns = sorted(anns)

            for ann in anns:
                ann_type = type(ann)

                # check for container
                is_sub_section = isinstance(ann, SubSectionAnnotation)
                if isinstance(ann, StartSectionAnnotation) or is_sub_section:
                    if is_sub_section:
                        if self.stack_depth > self.max_stack_depth:
                            logging.info(f"Stack ({self.stack_depth}) depth is at limit {self.max_stack_depth}.")
                            continue

                    settings = gui.CollapsableVert(ann.name, self.container_spacing, self.container_margins)
                    settings.set_is_open(not ann.collapsed)
                    grid = gui.VGrid(2, 0.25 * self.em)
                    settings.add_child(grid)

                    # implementation of active field link
                    if ann.is_active_field is not None:
                        if ann.is_active_field.value:
                            root_widget.add_child(settings)

                        if self.__on_recreate_requested not in ann.is_active_field.on_changed:
                            ann.is_active_field.on_changed += self.__on_recreate_requested
                    else:
                        root_widget.add_child(settings)

                    if is_sub_section:
                        self._create_properties(model.value, grid)
                        continue

                    containers.push(grid)
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
                    containers.peek().add_child(widget)

            if pop_after:
                containers.pop()

        # add all containers that are left
        while not containers.is_empty:
            root_widget.add_child(containers.pop())

        self.stack_depth -= 1
