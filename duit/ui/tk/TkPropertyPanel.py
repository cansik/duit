import logging
import tkinter as tk
import typing
from typing import Union, Optional

import customtkinter as ctk

from duit.collections.Stack import Stack
from duit.ui.BasePropertyPanel import BasePropertyPanel
from duit.ui.PropertyRegistry import UI_PROPERTY_REGISTRY
from duit.ui.annotations import find_all_ui_annotations
from duit.ui.annotations.container.EndSectionAnnotation import EndSectionAnnotation
from duit.ui.annotations.container.StartSectionAnnotation import StartSectionAnnotation
from duit.ui.tk.TkFieldProperty import TkFieldProperty


class TkPropertyPanel(BasePropertyPanel, ctk.CTkScrollableFrame):
    def __init__(self, master: Union[ctk.CTk, ctk.CTkFrame]):
        BasePropertyPanel.__init__(self)
        ctk.CTkScrollableFrame.__init__(self, master, corner_radius=0)

        self.tabview: Optional[ctk.CTkTabview] = None
        self.general_tab: Optional[ctk.CTkFrame] = None

        self._init_tab_view()

    def _init_tab_view(self):
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(padx=5, pady=5, fill=tk.BOTH)

        self.general_tab = self._add_tab("General")

    def _add_tab(self, title: str) -> ctk.CTkFrame:
        tab = self.tabview.add(title)
        tab.grid_columnconfigure(1, weight=1)
        return tab

    def _clean_widgets(self):
        for widget in self.winfo_children():
            widget.destroy()

        self._init_tab_view()

    def _create_panel(self):
        self._clean_widgets()

        containers: Stack[ctk.CTkFrame] = Stack()
        containers.push(self.general_tab)

        annotations = find_all_ui_annotations(self.data_context)
        row_counter = 0
        for var_name, (model, anns) in annotations.items():
            anns = sorted(anns)

            for ann in anns:
                ann_type = type(ann)

                if isinstance(ann, StartSectionAnnotation):
                    tab = self._add_tab(ann.name)
                    containers.push(tab)
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
