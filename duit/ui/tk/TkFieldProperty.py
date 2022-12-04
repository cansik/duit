from abc import ABC, abstractmethod
from typing import Generic, Optional, Iterable

from customtkinter.windows.widgets.core_widget_classes import CTkBaseClass

from duit.model.DataField import DataField, T
from duit.ui.annotations import UIAnnotation
import customtkinter as ctk

from duit.ui.tk.TkProperty import TkProperty


class TkFieldProperty(Generic[T], TkProperty[T], ABC):
    def __init__(self, annotation: UIAnnotation, model: Optional[DataField] = None, hide_label: bool = False):
        super().__init__(annotation, model)
        self.hide_label = hide_label

    def create_widgets(self, master) -> Iterable[CTkBaseClass]:
        if self.hide_label:
            return CTkBaseClass(master), self.create_field(master)

        return ctk.CTkLabel(master, text=f"{self.annotation.name}:"), self.create_field(master)

    @abstractmethod
    def create_field(self, master) -> CTkBaseClass:
        pass
