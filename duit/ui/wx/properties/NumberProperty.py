from typing import Optional

import wx

from duit.model.DataField import DataField
from duit.ui.annotations import NumberAnnotation
from duit.ui.wx.WxFieldProperty import WxFieldProperty
from duit.ui.wx.widgets.WxNumberField import WxNumberField


class NumberProperty(WxFieldProperty[NumberAnnotation, DataField]):
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

        field = WxNumberField(parent,
                              value=initial_value,
                              min_value=self.annotation.limit_min,
                              max_value=self.annotation.limit_max,
                              precision=self.annotation.decimal_precision,
                              integer_only=isinstance(initial_value, int))

        field.Enable(not self.annotation.read_only or self.annotation.copy_content)
        field.SetToolTip(self.annotation.tooltip)

        def on_dm_changed(value):
            def _update_ui():
                field.number_value = value

            self.silent_ui_update(_update_ui)

        def on_ui_changed(value):
            if self.is_ui_silent:
                return

            self.model.value = field.number_value

        self.model.on_changed.append(on_dm_changed)
        field.on_changed += on_ui_changed

        self.model.fire_latest()
        return field
