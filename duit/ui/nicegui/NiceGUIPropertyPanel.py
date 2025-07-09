import logging
from functools import partial
from typing import Any, Optional

from nicegui import ui
from nicegui.element import Element

from duit.ui.BasePropertyPanel import BasePropertyPanel
from duit.ui.PropertyRegistry import UI_PROPERTY_REGISTRY
from duit.ui.annotations import find_all_ui_annotations
from duit.ui.annotations.container.EndSectionAnnotation import EndSectionAnnotation
from duit.ui.annotations.container.StartSectionAnnotation import StartSectionAnnotation
from duit.ui.annotations.container.SubSectionAnnotation import SubSectionAnnotation


class NiceGUIPropertyPanel(Element, BasePropertyPanel):
    """
    A property panel that uses NiceGUI to render UI components 
    based on annotations of the given data context.

    Inherits from both Element and BasePropertyPanel.
    """

    def __init__(self):
        """
        Initializes the NiceGUIPropertyPanel with default parameters 
        for stack depth, data context, and grid layout settings.
        """
        super().__init__()

        self.max_stack_depth = 5
        self.stack_depth = 0

        self._data_context: Optional[Any] = None

        self._grid_columns = "auto 2fr"
        self._grid_classes = "w-full gap-1"

    def _create_panel(self):
        """
        Clears the panel and creates a new UI structure based 
        on the current data context. Initializes the root element 
        and calls the method to create properties.
        """
        self.clear()

        if self._data_context is None:
            return

        # add root element
        with self:
            root = ui.grid(columns=self._grid_columns).classes(self._grid_classes)

        # add elements to gui
        self._create_properties(self._data_context, root)

        self.update()

    def _create_properties(self, obj: Any, container: Element):
        """
        Recursively creates UI properties based on the annotations of 
        the provided object. It manages sections and sub-sections as 
        defined by StartSectionAnnotation and EndSectionAnnotation.

        :param obj: The object containing UI annotations.
        :param container: The container element to hold the created UI components.
        """
        self.stack_depth += 1
        container.__enter__()

        # Initial setup for non-section widgets
        current_container = container

        annotations = find_all_ui_annotations(obj)

        for var_name, (model, anns) in annotations.items():
            anns = sorted(anns)

            for ann in anns:
                ann_type = type(ann)

                is_sub_section = isinstance(ann, SubSectionAnnotation)
                if isinstance(ann, StartSectionAnnotation) or is_sub_section:
                    if is_sub_section:
                        if self.stack_depth > self.max_stack_depth:
                            logging.info(f"Stack ({self.stack_depth}) depth is at limit {self.max_stack_depth}.")
                            continue

                    # setup pane
                    expansion = ui.expansion(ann.name, value=not ann.collapsed)
                    (expansion.classes("w-full col-span-full")
                     .props('header-class="font-bold bg-gray-100 bg-opacity-50 dark:bg-gray-800 dark:bg-opacity-50"'))

                    with expansion:
                        root_grid = ui.grid(columns=self._grid_columns).classes(self._grid_classes)

                    root_grid.__enter__()

                    # implementation of active field link
                    if ann.is_active_field is not None:
                        ann.is_active_field.on_changed += partial(expansion.set_visibility)
                        ann.is_active_field.fire_latest()

                    if ann.name_field is not None:
                        ann.name_field.on_changed += partial(expansion.set_text)
                        ann.name_field.fire_latest()

                    if is_sub_section:
                        # add widgets and continue
                        self._create_properties(model.value, root_grid)
                        current_container.__exit__()
                        current_container = container
                        continue

                    current_container = root_grid
                    continue

                if isinstance(ann, EndSectionAnnotation):
                    current_container.__exit__()
                    current_container = container
                    continue

                if ann_type not in UI_PROPERTY_REGISTRY:
                    logging.warning(f"Annotation not registered: {ann_type.__name__}")
                    continue

                property_field = UI_PROPERTY_REGISTRY[ann_type](ann, model)
                _ = property_field.create_widgets()

        container.__exit__()
