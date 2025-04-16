from abc import ABC, abstractmethod
from typing import Generic, Optional, Iterable, Sequence, Callable

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
        self.is_ui_silent: bool = False

    def create_widgets(self, parent) -> Iterable[wx.Window]:
        """
        Creates wxPython widgets for this property.

        Args:
            parent: The parent widget.

        Returns:
            Iterable[wx.Window]: An iterable of wxPython widgets.
        """
        result = self.create_field(parent)

        if isinstance(result, Sequence):
            return result

        if self.hide_label:
            return [wx.Panel(parent), result]

        label = wx.StaticText(parent, label=f"{self.annotation.name}:")
        return label, result

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

    def silent_ui_update(self, handler: Callable, *args, **kwargs):
        def ui_task():
            self.is_ui_silent = True
            handler(*args, *kwargs)
            self.is_ui_silent = False

        wx.CallAfter(ui_task)
