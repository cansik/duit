from typing import Optional, Any, List

import wx

from duit.model.SelectableDataList import SelectableDataList
from duit.ui.annotations.ListAnnotation import ListAnnotation
from duit.ui.wx.WxFieldProperty import WxFieldProperty


class ListProperty(WxFieldProperty[ListAnnotation, SelectableDataList]):
    """
    Property class for handling ListAnnotation.

    This property generates a combobox or selection box widget for selecting from a list of options.
    """

    def __init__(self, annotation: ListAnnotation, model: Optional[SelectableDataList] = None):
        """
        Initialize a ListProperty.

        :param annotation: The ListAnnotation associated with this property.
        :param model: The data model for this property (default is None).
        """
        super().__init__(annotation, model)

    def create_field(self, parent) -> wx.ComboBox:
        """
        Create the field widget for the ListProperty.

        This method generates a combobox or selection box widget based on the platform, for selecting options from a list.

        :return: The combobox or selection box widget.
        """
        field = wx.ComboBox(parent, choices=[], style=wx.CB_DROPDOWN | wx.CB_READONLY)
        field.Enable(not self.annotation.read_only)
        field.SetToolTip(self.annotation.tooltip)

        def on_dm_changed(value):
            def update_ui():
                index = field.GetSelection()
                field.Clear()

                for option in self.options:
                    field.Append(self.get_option_name(option))

                field.SetSelection(index)

            wx.CallAfter(update_ui)

        def on_ui_selection_changed(event):
            index = field.GetSelection()
            if index != wx.NOT_FOUND:
                self.model.selected_index = index

        self.model.on_changed += on_dm_changed
        field.Bind(wx.EVT_COMBOBOX, on_ui_selection_changed)

        self.model.fire_latest()
        return field

    @property
    def options(self) -> List[Any]:
        """
        Get the list of available options.

        :return: A list of available options.
        """
        return self.model.value

    def get_option_name(self, option) -> str:
        """
        Get the name of an option.

        :param option: The option for which to retrieve the name.
        :return: The name of the option.
        """
        return str(option)
