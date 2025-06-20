from typing import Optional, List, Union

from nicegui.elements.input import Input
from nicegui.elements.mixins.validation_element import ValidationFunction, ValidationDict
from nicegui.events import Handler, ValueChangeEventArguments, GenericEventArguments

from duit.event.Event import Event


class InputTextField(Input):
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
        self.on_input_changed(self.value)
