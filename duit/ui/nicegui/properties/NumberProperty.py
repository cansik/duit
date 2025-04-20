from nicegui import ui
from nicegui.element import Element

from duit.model.DataField import DataField
from duit.ui.annotations import NumberAnnotation
from duit.ui.nicegui.NiceGUIFieldProperty import NiceGUIFieldProperty


class NumberProperty(NiceGUIFieldProperty[NumberAnnotation, DataField]):
    def create_field(self) -> Element:
        ann = self.annotation

        is_integer_only = isinstance(self.model.value, int)

        element = ui.number(
            value=self.model.value,
            min=ann.limit_min,
            max=ann.limit_max,
            precision=ann.decimal_precision
        ).props(self._default_props)

        element.set_enabled(not ann.read_only)

        if ann.tooltip is not None and ann.tooltip != "":
            element.tooltip(ann.tooltip)

        # todo: Also implement ann.copy_content

        def on_ui_changed(*args, **kwargs):
            with self.silent() as ok:
                if not ok:
                    return

                if is_integer_only:
                    self.model.value = int(element.value)
                else:
                    self.model.value = float(element.value)

        def on_model_changed(value: str):
            with self.silent() as ok:
                if not ok:
                    return

                if is_integer_only:
                    element.value = int(value)
                else:
                    element.value = float(value)

        element.on("keydown.enter", on_ui_changed)
        element.on("blur", on_ui_changed)

        self.model.on_changed += on_model_changed
        self.model.fire_latest()

        return element
