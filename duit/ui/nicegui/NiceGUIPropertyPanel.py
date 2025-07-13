import logging
from functools import partial
from typing import Any, Optional

from nicegui import ui
from nicegui.element import Element

from duit.ui.BasePropertyPanel import BasePropertyPanel
from duit.ui.PropertyRegistry import UI_PROPERTY_REGISTRY
from duit.ui.annotations.container.StartSectionAnnotation import StartSectionAnnotation
from duit.ui.annotations.container.SubSectionAnnotation import SubSectionAnnotation
from duit.ui.meta import meta_utils
from duit.ui.meta.MetaNode import MetaNode
from duit.ui.nicegui.NiceGUIProperty import NiceGUIProperty


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
        Creates and renders the property panel UI.

        Clears the current content, constructs a meta-tree from the data context,
        and renders the UI components recursively using the meta-tree nodes.
        """
        self.clear()
        if self._data_context is None:
            return

        # root container
        with self:
            root = ui.grid(columns=self._grid_columns).classes(self._grid_classes)

        # build meta‐tree
        meta_tree = meta_utils.build_meta_tree(self._data_context)

        # render it
        self._render_meta_nodes(meta_tree, root, depth=0)

        self.update()

    def _render_meta_nodes(self, nodes: list[MetaNode], container: Element, depth: int):
        """
        Recursively render a list of MetaNode into the given NiceGUI container.
        Supports StartSectionAnnotation, SubSectionAnnotation, and leaf‐field annotations.

        :param nodes: A list of MetaNode objects to be rendered.
        :param container: The NiceGUI container element where nodes will be rendered.
        :param depth: The current depth in the recursive rendering hierarchy.
        """
        # prevent too‐deep nesting
        if depth > self.max_stack_depth:
            logging.info(f"Maximum nesting depth ({self.max_stack_depth}) reached; skipping deeper nodes.")
            return

        # enter the container context (grid or expansion)
        container.__enter__()

        for node in nodes:
            ann = node.annotation
            model = node.model

            # SECTION or SUBSECTION
            if isinstance(ann, (StartSectionAnnotation, SubSectionAnnotation)):
                # create an expansion pane
                expansion = ui.expansion(ann.name, value=not ann.collapsed) \
                    .classes("w-full col-span-full") \
                    .props('header-class="font-bold bg-gray-100 bg-opacity-50 dark:bg-gray-800 dark:bg-opacity-50"'
                           )

                # begin the expansion context
                with expansion:
                    # inside each section/subsection we use a grid
                    grid = ui.grid(columns=self._grid_columns) \
                        .classes(self._grid_classes)

                # manually enter the grid context so we can exit later
                grid.__enter__()

                # link expansion visibility to an "active" field, if provided
                if getattr(ann, "is_active_field", None) is not None:
                    ann.is_active_field.on_changed += partial(expansion.set_visibility)
                    ann.is_active_field.fire_latest()

                # link expansion title to a "name" field, if provided
                if getattr(ann, "name_field", None) is not None:
                    ann.name_field.on_changed += partial(expansion.set_text)
                    ann.name_field.fire_latest()

                # recurse into nested nodes
                self._render_meta_nodes(node.children, grid, depth + 1)

                # exit the grid context
                grid.__exit__()
                continue

            # LEAF FIELD
            renderer_cls = UI_PROPERTY_REGISTRY.get(type(ann))
            if renderer_cls is None:
                logging.warning(f"Annotation not registered: {type(ann).__name__}")
                continue

            # create the actual property widget(s)
            property_field: NiceGUIProperty = renderer_cls(ann, model)
            property_field.create_widgets()

        # exit the container context
        container.__exit__()
