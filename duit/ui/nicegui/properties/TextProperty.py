from nicegui import ui
from nicegui.element import Element

from duit.model.DataField import DataField
from duit.ui.annotations.TextAnnotation import TextAnnotation
from duit.ui.nicegui.NiceGUIFieldProperty import NiceGUIFieldProperty


class TextProperty(NiceGUIFieldProperty[TextAnnotation, DataField]):
    def create_field(self) -> Element:
        ann = self.annotation

        element = ui.input(placeholder=ann.placeholder_text).props("rounded outlined dense")

        element.set_enabled(not ann.read_only)
        element.set_autocomplete([])
        element.tooltip(ann.tooltip)

        # todo: Also implement ann.copy_content

        def on_ui_changed(*args, **kwargs):
            if self.is_ui_silent:
                return

            self.is_ui_silent = True
            self.model.value = element.value
            self.is_ui_silent = False

        def on_model_changed(value: str):
            if self.is_ui_silent:
                return

            self.is_ui_silent = True
            element.value = str(value)
            self.is_ui_silent = False

        element.on("keydown.enter", on_ui_changed)
        element.on("blur", on_ui_changed)
        self.model.on_changed += on_model_changed

        return element
