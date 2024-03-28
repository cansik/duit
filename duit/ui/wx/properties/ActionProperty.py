import wx
import threading
from typing import Optional

from duit.model.DataField import DataField
from duit.ui.annotations.ActionAnnotation import ActionAnnotation
from duit.ui.wx.WxFieldProperty import WxFieldProperty


class ActionProperty(WxFieldProperty[ActionAnnotation, DataField]):
    def __init__(self, annotation: ActionAnnotation, model: Optional[DataField] = None):
        """
        Initialize an ActionProperty.

        Args:
            annotation (ActionAnnotation): The ActionAnnotation associated with the property.
            model (Optional[DataField]): The model object for the property, if applicable.
        """
        super().__init__(annotation, model)

    def create_field(self, parent) -> wx.Button:
        """
        Create and return the GUI field for the action property.

        Args:
            parent: The parent widget where the field will be created.

        Returns:
            wx.Button: The created GUI field.
        """
        field = wx.Button(parent, label=self.annotation.text)
        field.SetToolTip(self.annotation.tooltip)

        def on_clicked(event):
            if self.model is None:
                return

            if self.annotation.threaded:
                thread = threading.Thread(target=self._run_method, daemon=True)
                thread.start()
            else:
                self._run_method()

        field.Bind(wx.EVT_BUTTON, on_clicked)
        return field

    def _run_method(self):
        """
        Run the action method associated with the property.
        """
        self.model.value()
