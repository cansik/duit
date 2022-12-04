from abc import ABC, abstractmethod
from typing import Generic, Optional, Iterable

from customtkinter.windows.widgets.core_widget_classes import CTkBaseClass

from duit.model.DataField import DataField, T
from duit.ui.annotations import UIAnnotation
import customtkinter as ctk

from duit.ui.tk.TkProperty import TkProperty


class TkFieldProperty(Generic[T], TkProperty[T], ABC):
    def __init__(self, annotation: UIAnnotation, model: Optional[DataField] = None):
        super().__init__(annotation, model)

    def create_widgets(self, master) -> Iterable[CTkBaseClass]:
        return ctk.CTkLabel(master, text=f"{self.annotation.name}:"), self.create_field(master)

    @abstractmethod
    def create_field(self, master) -> CTkBaseClass:
        pass
