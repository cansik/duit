import logging
import tkinter as tk
import typing
from typing import Union

import customtkinter as ctk

from duit.collections.Stack import Stack
from duit.ui.BasePropertyPanel import BasePropertyPanel
from duit.ui.PropertyRegistry import UI_PROPERTY_REGISTRY
from duit.ui.annotations import find_all_ui_annotations
from duit.ui.annotations.container.EndSectionAnnotation import EndSectionAnnotation
from duit.ui.annotations.container.StartSectionAnnotation import StartSectionAnnotation
from duit.ui.tk.TkFieldProperty import TkFieldProperty
from duit.ui.tk.widgets.CTkCollapsable import CTkCollapsable


class TkPropertyPanel(BasePropertyPanel, ctk.CTkScrollableFrame):
    def __init__(self, master: Union[ctk.CTk, ctk.CTkFrame]):
        """
        Initializes a TkPropertyPanel.

        Args:
            master (Union[ctk.CTk, ctk.CTkFrame]): The parent widget.
        """
        BasePropertyPanel.__init__(self)
        ctk.CTkScrollableFrame.__init__(self, master, corner_radius=0)

        # self.pack(padx=5, pady=5, fill=tk.BOTH)

        self.frame: typing.Optional[ctk.CTkFrame] = None
        self._clean_widgets()

    def _clean_widgets(self):
        """
        Clear the widgets in the property panel.
        """
        for widget in self.winfo_children():
            widget.destroy()

        self.frame = ctk.CTkFrame(self)
        self.frame.pack(padx=5, pady=5, fill=tk.BOTH)
        self.frame.grid_columnconfigure(1, weight=1)

    def _create_panel(self):
        """
        Create the property panel with the widgets based on the annotations.
        """
        self._clean_widgets()

        containers: Stack[tk.Frame] = Stack()
        containers.push(self.frame)

        annotations = find_all_ui_annotations(self.data_context)
        row_counter = 0
        for var_name, (model, anns) in annotations.items():
            anns = sorted(anns)

            for ann in anns:
                ann_type = type(ann)

                if isinstance(ann, StartSectionAnnotation):
                    collapsable = CTkCollapsable(master=containers.peek(), text=ann.name, shown=not ann.collapsed)
                    collapsable.grid(row=row_counter, column=0, pady=4, columnspan=2, sticky="we")
                    collapsable.frame.grid_columnconfigure(1, weight=1)
                    collapsable.frame.pack()
                    containers.push(collapsable.frame)

                    row_counter += 1
                    continue

                if isinstance(ann, EndSectionAnnotation):
                    containers.pop()
                    continue

                if ann_type not in UI_PROPERTY_REGISTRY:
                    logging.warning(f"Annotation not registered: {ann_type.__name__}")
                    continue

                # add property
                property_field = typing.cast(TkFieldProperty, UI_PROPERTY_REGISTRY[ann_type](ann, model))
                widgets = property_field.create_widgets(containers.peek())

                for i, widget in enumerate(widgets):
                    extra = {}
                    if i == 1:
                        extra = {
                            "sticky": "we",
                            "padx": 20,
                        }

                    widget.grid(row=row_counter, column=i, pady=4, **extra)
                row_counter += 1
