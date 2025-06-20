from typing import List, Any

from nicegui import ui
from nicegui.element import Element

from duit.model.SelectableDataList import SelectableDataList
from duit.ui.BaseProperty import BaseProperty
from duit.ui.annotations.ListAnnotation import ListAnnotation
from duit.ui.nicegui.NiceGUIFieldProperty import NiceGUIFieldProperty


class ListProperty(NiceGUIFieldProperty[ListAnnotation, SelectableDataList]):
    """
    A property class representing a list field with selectable options.
    """

    def create_field(self) -> Element:
        """
        Creates the UI field for the list property.

        :return: An Element representing the selectable options in the UI.
        """
        ann = self.annotation

        element = ui.select([]).props(self._default_props)

        if self.annotation.read_only:
            element.props("readonly")

        if ann.tooltip is not None and ann.tooltip != "":
            element.tooltip(ann.tooltip)

        @BaseProperty.suppress_updates
        def on_ui_changed(*args, **kwargs):
            value = element.value
            self.model.selected_index = [self.get_option_name(e) for e in self.model.value].index(value)

        @BaseProperty.suppress_updates
        def on_model_changed(*args, **kwargs):
            element.set_options([self.get_option_name(e) for e in self.model.value],
                                value=self.get_option_name(self.model.selected_item))
            element.update()

        @BaseProperty.suppress_updates
        def on_index_changed(index: int):
            element.value = self.get_option_name(self.model.value[index])

        element.on_value_change(on_ui_changed)

        self.model.on_changed += on_model_changed
        self.model.on_index_changed += on_index_changed
        self.model.fire_latest()

        return element

    @property
    def options(self) -> List[Any]:
        """
        Get the list of available options.

        :return: A list of available options.
        """
        return self.model.value

    def get_option_name(self, option: str) -> str:
        """
        Get the name of an option.

        :param option: The option for which to retrieve the name.
        :return: The name of the option.
        """
        return str(option)
