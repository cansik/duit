from typing import Optional

import wx

from duit.model.DataField import DataField
from duit.ui.annotations import NumberAnnotation
from duit.ui.wx.WxFieldProperty import WxFieldProperty


class NumberProperty(WxFieldProperty[NumberAnnotation, DataField]):
    MAX_INT32 = 2 ** 31 - 1
    MIN_INT32 = 2 ** 31 * -1

    """
    Property class for handling NumberAnnotation.

    This property generates a numeric input field for editing numeric values.

    """

    def __init__(self, annotation: NumberAnnotation, model: Optional[DataField] = None):
        """
        Initialize a NumberProperty.

        :param annotation: The NumberAnnotation associated with this property.
        :param model: The data model for this property (default is None).
        """
        super().__init__(annotation, model)

    def create_field(self, parent: wx.Window) -> wx.Control:
        """
        Create the field widget for the NumberProperty.

        This method generates a numeric input field (int or double) for editing numeric values.

        :param parent: Parent window for the field widget.
        :return: The numeric input field widget.
        """
        initial_value = self.model.value

        if isinstance(initial_value, int):
            field = wx.SpinCtrl(parent, value=str(initial_value), size=(100, -1))
        else:
            field = wx.SpinCtrlDouble(parent, value=str(initial_value), size=(100, -1))
            field.SetDigits(self.annotation.decimal_precision)

        field.SetRange(max(self.annotation.limit_min, self.MIN_INT32), min(self.annotation.limit_max, self.MAX_INT32))

        field.Enable(not self.annotation.read_only or self.annotation.copy_content)
        field.SetToolTip(self.annotation.tooltip)

        def on_dm_changed(value):
            field.SetValue(value)

        def on_ui_changed(_):
            self.model.value = field.GetValue()

        self.model.on_changed.append(on_dm_changed)

        field.Bind(wx.EVT_SPINCTRL, on_ui_changed)
        field.Bind(wx.EVT_SPINCTRLDOUBLE, on_ui_changed)

        self.model.fire_latest()
        return field
