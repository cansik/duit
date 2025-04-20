from nicegui import ui
from nicegui.element import Element

from duit.model.DataField import DataField
from duit.ui.annotations.TextAnnotation import TextAnnotation
from duit.ui.nicegui.NiceGUIFieldProperty import NiceGUIFieldProperty


class TextProperty(NiceGUIFieldProperty[TextAnnotation, DataField]):
    def create_field(self) -> Element:
        ann = self.annotation

        element = ui.input(placeholder=ann.placeholder_text).props(self._default_props)

        element.set_enabled(not ann.read_only)
        element.set_autocomplete([])

        if ann.tooltip is not None and ann.tooltip != "":
            element.tooltip(ann.tooltip)

        # todo: Also implement ann.copy_content

        def on_ui_changed(*args, **kwargs):
            with self.silent() as ok:
                if not ok:
                    return

                self.model.value = element.value

        def on_model_changed(value: str):
            with self.silent() as ok:
                if not ok:
                    return

                element.value = str(value)

        element.on("keydown.enter", on_ui_changed)
        element.on("blur", on_ui_changed)

        self.model.on_changed += on_model_changed
        self.model.fire_latest()

        return element
