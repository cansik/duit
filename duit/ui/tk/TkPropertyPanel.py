import logging
from typing import Union

import customtkinter as ctk

from duit.ui.BasePropertyPanel import BasePropertyPanel
from duit.ui.PropertyRegistry import UI_PROPERTY_REGISTRY
from duit.ui.annotations import find_all_ui_annotations
from duit.ui.tk.TkFieldProperty import TkFieldProperty


class TkPropertyPanel(BasePropertyPanel, ctk.CTkFrame):
    def __init__(self, master: Union[ctk.CTk, ctk.CTkFrame]):
        BasePropertyPanel.__init__(self)
        ctk.CTkFrame.__init__(self, master, corner_radius=0)

        self.grid_columnconfigure(1, weight=1)

    def _clean_widgets(self):
        for widget in self.winfo_children():
            widget.destroy()

    def _create_panel(self):
        self._clean_widgets()

        annotations = find_all_ui_annotations(self.data_context)
        row_counter = 0
        for var_name, (model, anns) in annotations.items():
            for ann in anns:
                ann_type = type(ann)

                if ann_type not in UI_PROPERTY_REGISTRY:
                    logging.warning(f"Annotation not registered: {ann_type.__name__}")
                    continue

                # add property
                property_field = UI_PROPERTY_REGISTRY[ann_type](ann, model)  # type: TkFieldProperty
                widgets = property_field.create_widgets(self)

                for i, widget in enumerate(widgets):
                    extra = {}
                    if i == 1:
                        extra = {
                            "sticky": "we",
                            "padx": 20,
                        }

                    widget.grid(row=row_counter, column=i, pady=4, **extra)
                row_counter += 1
