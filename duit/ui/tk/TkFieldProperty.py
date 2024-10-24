from abc import ABC, abstractmethod
from typing import Generic, Optional, Iterable

import customtkinter as ctk
from customtkinter.windows.widgets.core_widget_classes import CTkBaseClass

from duit.model.DataField import T
from duit.ui.BaseProperty import M
from duit.ui.annotations import UIAnnotation
from duit.ui.tk.TkProperty import TkProperty


class TkFieldProperty(Generic[T, M], TkProperty[T, M], ABC):
    def __init__(self, annotation: UIAnnotation, model: Optional[M] = None, hide_label: bool = False):
        """
        Initializes a TkFieldProperty.

        Args:
            annotation (UIAnnotation): The UI annotation associated with this property.
            model (Optional[M], optional): The model to link with the property. Defaults to None.
            hide_label (bool, optional): Whether to hide the label. Defaults to False.
        """
        super().__init__(annotation, model)
        self.hide_label = hide_label

    def create_widgets(self, master) -> Iterable[CTkBaseClass]:
        """
        Creates Tkinter widgets for this property.

        Args:
            master: The parent widget.

        Returns:
            Iterable[CTkBaseClass]: An iterable of Tkinter widgets.
        """
        if self.hide_label:
            return CTkBaseClass(master), self.create_field(master)

        return ctk.CTkLabel(master, text=f"{self.annotation.name}:"), self.create_field(master)

    @abstractmethod
    def create_field(self, master) -> CTkBaseClass:
        """
        Creates the specific field widget for this property.

        Args:
            master: The parent widget.

        Returns:
            CTkBaseClass: The field widget.
        """
        pass
