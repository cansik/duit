from typing import Optional, List, Union

from nicegui.elements.input import Input
from nicegui.elements.mixins.validation_element import ValidationFunction, ValidationDict
from nicegui.events import Handler, ValueChangeEventArguments, GenericEventArguments

from duit.event.Event import Event


class InputTextField(Input):
    """
    A text input field that supports various input configurations such as placeholder, password toggle, 
    and validation.

    :param label: Optional label for the input field.
    :param placeholder: Optional placeholder text displayed when the input is empty.
    :param value: The initial value of the input field, default is an empty string.
    :param password: If True, the input field will hide the text for password entry.
    :param password_toggle_button: If True, adds a button to toggle password visibility.
    :param on_change: Optional event handler for value change events.
    :param autocomplete: Optional list of suggested autocomplete options.
    :param validation: Optional validation function or dictionary for input validation.
    """

    def __init__(self,
                 label: Optional[str] = None, *,
                 placeholder: Optional[str] = None,
                 value: str = '',
                 password: bool = False,
                 password_toggle_button: bool = False,
                 on_change: Optional[Handler[ValueChangeEventArguments]] = None,
                 autocomplete: Optional[List[str]] = None,
                 validation: Optional[Union[ValidationFunction, ValidationDict]] = None,
                 ) -> None:
        super().__init__(label, placeholder=placeholder, value=value, password=password,
                         password_toggle_button=password_toggle_button, on_change=on_change, autocomplete=autocomplete,
                         validation=validation)
        self.set_autocomplete([])

        self.on_input_changed: Event[str] = Event()

        self.on("keydown.enter", self._call_event)
        self.on("blur", self._call_event)

    def _call_event(self, _: GenericEventArguments):
        """
        Triggers the input change event with the current value of the input field.

        :param _: Generic event arguments for input change events.
        """
        self.on_input_changed(self.value)
