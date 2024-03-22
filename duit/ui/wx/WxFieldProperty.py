from abc import ABC, abstractmethod
from typing import Generic, Optional, Iterable

import wx

from duit.model.DataField import T
from duit.ui.BaseProperty import M
from duit.ui.annotations import UIAnnotation
from duit.ui.wx.WxProperty import WxProperty


class WxFieldProperty(Generic[T, M], WxProperty[T, M], ABC):

    def __init__(self, annotation: UIAnnotation, model: Optional[M] = None, hide_label: bool = False):
        """
        Initializes a WxFieldProperty.

        Args:
            annotation (UIAnnotation): The UI annotation associated with this property.
            model (Optional[M], optional): The model to link with the property. Defaults to None.
            hide_label (bool, optional): Whether to hide the label. Defaults to False.
        """
        super().__init__(annotation, model)
        self.hide_label = hide_label

    def create_widgets(self, parent) -> Iterable[wx.Window]:
        """
        Creates wxPython widgets for this property.

        Args:
            parent: The parent widget.

        Returns:
            Iterable[wx.Window]: An iterable of wxPython widgets.
        """
        if self.hide_label:
            return [self.create_field(parent)]

        label = wx.StaticText(parent, label=f"{self.annotation.name}:")
        field = self.create_field(parent)
        return label, field

    @abstractmethod
    def create_field(self, parent) -> wx.Window:
        """
        Creates the specific field widget for this property.

        Args:
            parent: The parent widget.

        Returns:
            wx.Window: The field widget.
        """
        pass
