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

    def __init__(self):
        super().__init__()

        self.max_stack_depth = 5
        self.stack_depth = 0

        self._data_context: Optional[Any] = None

    def _create_panel(self):
        # remove all children
        self.clear()

        if self._data_context is None:
            return

        # add root element
        with self:
            root = ui.grid(columns=2)

        # add elements to gui
        self._create_properties(self._data_context, root)

        self.update()

    def _create_properties(self, obj: Any, container: Element):
        self.stack_depth += 1
        container.__enter__()

        # Initial setup for non-section widgets
        current_container = container

        annotations = find_all_ui_annotations(obj)

        in_section = False
        for var_name, (model, anns) in annotations.items():
            anns = sorted(anns)
            in_section = False

            for ann in anns:
                ann_type = type(ann)

                is_sub_section = isinstance(ann, SubSectionAnnotation)
                if isinstance(ann, StartSectionAnnotation) or is_sub_section:
                    if is_sub_section:
                        if self.stack_depth > self.max_stack_depth:
                            logging.info(f"Stack ({self.stack_depth}) depth is at limit {self.max_stack_depth}.")
                            continue

                    # setup pane
                    expansion = ui.expansion(ann.name, value=ann.collapsed).classes("w-full col-span-full")
                    with expansion:
                        root_grid = ui.grid(columns=2)

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
                        continue

                    current_container = root_grid
                    in_section = True
                    continue

                if isinstance(ann, EndSectionAnnotation):
                    current_container.__exit__()
                    in_section = False
                    current_container = container
                    continue

                if ann_type not in UI_PROPERTY_REGISTRY:
                    logging.warning(f"Annotation not registered: {ann_type.__name__}")
                    continue

                property_field = UI_PROPERTY_REGISTRY[ann_type](ann, model)
                widgets = property_field.create_widgets()

        container.__exit__()
