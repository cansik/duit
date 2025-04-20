import threading
from typing import Optional

from nicegui import ui
from nicegui.element import Element

from duit.annotation.Annotation import M
from duit.model.DataField import DataField
from duit.ui.annotations import UIAnnotation
from duit.ui.annotations.ActionAnnotation import ActionAnnotation
from duit.ui.nicegui.NiceGUIFieldProperty import NiceGUIFieldProperty


class ActionProperty(NiceGUIFieldProperty[ActionAnnotation, DataField]):
    def __init__(self, annotation: UIAnnotation, model: Optional[M] = None, hide_label: bool = False):

        super().__init__(annotation, model, hide_label=True)

    def create_field(self) -> Element:
        ann = self.annotation

        element = ui.button(ann.text).props(self._default_props).classes("col-span-full")
        element.set_enabled(not ann.read_only)

        if ann.tooltip is not None and ann.tooltip != "":
            element.tooltip(ann.tooltip)

        def on_clicked(_):
            if self.model is None:
                return

            if self.annotation.threaded:
                thread = threading.Thread(target=self._run_method, daemon=True)
                thread.start()
            else:
                self._run_method()

        element.on_click(on_clicked)

        return element

    def _run_method(self):
        """
        Run the action method associated with the property.
        """
        self.model.value()
