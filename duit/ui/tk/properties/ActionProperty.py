import threading
from typing import Optional

from customtkinter import CTkButton
from customtkinter.windows.widgets.core_widget_classes import CTkBaseClass

from duit.model.DataField import DataField
from duit.ui.annotations.ActionAnnotation import ActionAnnotation
from duit.ui.tk.TkFieldProperty import TkFieldProperty


class ActionProperty(TkFieldProperty[ActionAnnotation]):
    def __init__(self, annotation: ActionAnnotation, model: Optional[DataField] = None):
        super().__init__(annotation, model, hide_label=not annotation.show_label)

    def create_field(self, master) -> CTkBaseClass:
        field = CTkButton(master, text=self.annotation.text)
        field.tooltip = self.annotation.tooltip

        def on_clicked():
            if self.model is None:
                return

            if self.annotation.threaded:
                thread = threading.Thread(target=self._run_method, daemon=True)
                thread.start()
            else:
                self._run_method()

        field.configure(command=on_clicked)
        return field

    def _run_method(self):
        self.model.value()
