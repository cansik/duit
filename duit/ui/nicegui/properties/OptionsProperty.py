from typing import List, Any

from nicegui import ui
from nicegui.element import Element

from duit.model.SelectableDataList import SelectableDataList
from duit.ui.BaseProperty import BaseProperty
from duit.ui.annotations.OptionsAnnotation import OptionsAnnotation
from duit.ui.nicegui.NiceGUIFieldProperty import NiceGUIFieldProperty


class OptionsProperty(NiceGUIFieldProperty[OptionsAnnotation, SelectableDataList]):
    def create_field(self) -> Element:
        ann = self.annotation

        options_str = [self.get_option_name(e) for e in self.options]
        element = ui.select(options_str, value=options_str[0]).props(self._default_props)

        if self.annotation.read_only:
            element.props("readonly")

        if ann.tooltip is not None and ann.tooltip != "":
            element.tooltip(ann.tooltip)

        @BaseProperty.suppress_updates
        def on_ui_changed(*args, **kwargs):
            value = element.value
            self.model.value = self.options[options_str.index(value)]

        @BaseProperty.suppress_updates
        def on_model_changed(value):
            if value in self.options:
                element.value = self.get_option_name(value)

        element.on_value_change(on_ui_changed)
        self.model.on_changed += on_model_changed
        self.model.fire_latest()

        return element

    @property
    def options(self) -> List[Any]:
        """
        Get the list of available options.

        :return: A list of available options.
        """
        return list(self.annotation.options)

    def get_option_name(self, option: str) -> str:
        """
        Get the name of an option.

        :param option: The option for which to retrieve the name.
        :return: The name of the option.
        """
        return str(option)
