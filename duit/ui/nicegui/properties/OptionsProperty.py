from typing import List, Any

from nicegui import ui
from nicegui.element import Element

from duit.model.SelectableDataList import SelectableDataList
from duit.ui.annotations.OptionsAnnotation import OptionsAnnotation
from duit.ui.nicegui.NiceGUIFieldProperty import NiceGUIFieldProperty
from duit.ui.nicegui.NiceGUIPropertyBinder import NiceGUIPropertyBinder


class OptionsProperty(NiceGUIFieldProperty[OptionsAnnotation, SelectableDataList]):
    """
    A property class that manages a selectable list of options in the NiceGUI framework.
    
    This class is responsible for creating a UI field that allows users to select from a list of options 
    and ensuring that the model's value is synchronized with the selected option.
    """

    def create_field(self) -> Element:
        """
        Creates a UI field for selecting options.

        This method creates a selectable UI element with the available options and sets up listeners 
        for changes in the UI and model.

        :return: An Element representing the selectable field in the UI.
        """
        ann = self.annotation

        options_str = [self.get_option_name(e) for e in self.options]
        element = ui.select(options_str, value=options_str[0]).props(self._default_props)

        if ann.read_only:
            element.props("readonly")

        if ann.tooltip:
            element.tooltip(ann.tooltip)

        def register_ui_change(cb):
            element.on_value_change(lambda ev: cb(ev.value))

        def to_model(value: str) -> Any:
            return self.options[options_str.index(value)]

        def to_ui(value: Any) -> str:
            if value in self.options:
                return self.get_option_name(value)
            return options_str[0] if options_str else ""

        self._binder = NiceGUIPropertyBinder[Any](
            element=element,
            model=self.model,
            register_ui_change=register_ui_change,
            to_model=to_model,
            to_ui=to_ui,
        )

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
