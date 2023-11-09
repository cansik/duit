from typing import Optional, Dict

import customtkinter as ctk
from customtkinter.windows.widgets.core_widget_classes import CTkBaseClass

from duit.model.DataField import DataField
from duit.ui.annotations.VectorAnnotation import VectorAnnotation
from duit.ui.tk.TkFieldProperty import TkFieldProperty
from duit.ui.tk.widgets.CTkNumberEntry import CTkNumberEntry
from duit.utils import _vector


class VectorProperty(TkFieldProperty[VectorAnnotation, DataField]):
    def __init__(self, annotation: VectorAnnotation, model: Optional[DataField] = None):
        """
        Initialize a VectorProperty instance.

        Args:
            annotation (VectorAnnotation): The vector annotation associated with this property.
            model (Optional[DataField]): The data model for this property.
        """
        super().__init__(annotation, model)

    def create_field(self, master) -> CTkBaseClass:
        """
        Create a vector input field for the given vector annotation.

        Args:
            master: The parent widget.

        Returns:
            CTkBaseClass: The created vector input field.
        """
        vector_attributes = _vector.get_vector_attributes(self.model.value)
        attribute_widgets: Dict[str, CTkNumberEntry] = {}

        container = ctk.CTkFrame(master, fg_color="transparent", corner_radius=0)

        labels = vector_attributes
        if self.annotation.labels is not None:
            assert len(labels) == len(self.annotation.labels), f"Label count is not correct for {self.annotation.name}!"
            labels = self.annotation.labels

        def update_model():
            for attribute_name in vector_attributes:
                setattr(self.model.value, attribute_name, attribute_widgets[attribute_name].value)
            self.model.fire()

        def update_ui():
            value = self.model.value
            for attribute_name in vector_attributes:
                attribute_widgets[attribute_name].value = getattr(value, attribute_name)

        column_index = 0
        for i, attribute_name in enumerate(vector_attributes):
            field = CTkNumberEntry(container, 0.0, decimal_precision=self.annotation.decimal_precision,
                                   width=self.annotation.max_width)
            field.enabled = not self.annotation.read_only or self.annotation.copy_content
            field.tooltip = self.annotation.tooltip

            def on_ui_changed(value):
                if self.annotation.read_only:
                    update_ui()
                else:
                    update_model()

            field.on_changed(on_ui_changed)

            label = labels[i]
            if self.annotation.hide_labels:
                field.tooltip = f"{label}"
            else:
                label_field = ctk.CTkLabel(container, text=f"{label}:")
                label_field.grid(row=0, column=column_index, padx=0, pady=0, sticky="e")
                column_index += 1

            field.grid(row=0, column=column_index, padx=self.annotation.spacing, pady=0, sticky="ew")
            container.grid_columnconfigure(column_index, weight=1)
            column_index += 1

            attribute_widgets[attribute_name] = field

        def on_dm_changed(value):
            update_ui()

        self.model.on_changed.append(on_dm_changed)
        self.model.fire_latest()

        return container
