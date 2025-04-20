from nicegui import ui
from nicegui.element import Element

from duit.model.DataField import DataField
from duit.ui.annotations.BooleanAnnotation import BooleanAnnotation
from duit.ui.nicegui.NiceGUIFieldProperty import NiceGUIFieldProperty


class BooleanProperty(NiceGUIFieldProperty[BooleanAnnotation, DataField]):
    def create_field(self) -> Element:
        ann = self.annotation

        element = ui.switch()
        element.set_enabled(not ann.read_only)

        if ann.tooltip is not None and ann.tooltip != "":
            element.tooltip(ann.tooltip)

        # todo: Also implement ann.copy_content

        def on_ui_changed(*args, **kwargs):
            with self.silent() as ok:
                if not ok:
                    return

                self.model.value = element.value

        def on_model_changed(value: bool):
            with self.silent() as ok:
                if not ok:
                    return

                element.value = bool(value)

        element.on_value_change(on_ui_changed)

        self.model.on_changed += on_model_changed
        self.model.fire_latest()

        return element
