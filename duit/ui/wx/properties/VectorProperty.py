from typing import Optional, Dict, Union

import wx
from wx import BoxSizer

from duit.model.DataField import DataField
from duit.ui.annotations.VectorAnnotation import VectorAnnotation
from duit.ui.wx.WxFieldProperty import WxFieldProperty
from duit.ui.wx.widgets.WxNumberField import WxNumberField
from duit.utils import _vector


class VectorProperty(WxFieldProperty[VectorAnnotation, DataField]):
    def __init__(self, annotation: VectorAnnotation, model: Optional[DataField] = None):
        """
        Initializes a VectorProperty instance.

        Args:
            annotation (VectorAnnotation): The VectorAnnotation associated with this property.
            model (Optional[DataField]): The data model field to bind this property to.
        """
        super().__init__(annotation, model)

    def create_field(self, parent: wx.Window) -> BoxSizer:
        """
        Create a vector entry widget for the given vector annotation in wxPython.

        Args:
            parent: The parent wxPython widget.

        Returns:
            wx.Window: The created vector entry widget.
        """
        vector_attributes = _vector.get_vector_attributes(self.model.value)
        attribute_widgets: Dict[str, WxNumberField] = {}

        container = wx.BoxSizer(orient=wx.HORIZONTAL)

        labels = vector_attributes
        if self.annotation.labels is not None:
            assert len(labels) == len(self.annotation.labels), f"Label count is not correct for {self.annotation.name}!"
            labels = self.annotation.labels

        def update_model():
            if self.is_ui_silent:
                return

            for attribute_name in vector_attributes:
                setattr(self.model.value, attribute_name, attribute_widgets[attribute_name].number_value)
            self.model.fire()

        def update_ui():
            value = self.model.value

            def _update_handler():
                for attribute_name in vector_attributes:
                    attribute_widgets[attribute_name].number_value = getattr(value, attribute_name)

            self.silent_ui_update(_update_handler)

        for i, attribute_name in enumerate(vector_attributes):
            field = WxNumberField(parent, size=(self.annotation.max_width, -1))
            field.precision = self.annotation.decimal_precision

            field.Enable(not self.annotation.read_only or self.annotation.copy_content)
            field.SetToolTip(self.annotation.tooltip)

            def on_ui_changed(value: Union[int, float]):
                if self.annotation.read_only:
                    update_ui()
                else:
                    update_model()

            field.on_changed.append(on_ui_changed)

            label = labels[i]

            if self.annotation.hide_labels:
                field.SetToolTip(f"{label}")
            else:
                label = wx.StaticText(parent, label=f"{label}:")
                container.Add(label, flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL, border=5)
            container.Add(field, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)

            attribute_widgets[attribute_name] = field

        def on_dm_changed(value):
            update_ui()

        self.model.on_changed.append(on_dm_changed)
        self.model.fire_latest()

        return container
