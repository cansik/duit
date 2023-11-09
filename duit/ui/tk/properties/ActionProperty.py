import threading
from typing import Optional

from customtkinter import CTkButton
from customtkinter.windows.widgets.core_widget_classes import CTkBaseClass

from duit.model.DataField import DataField
from duit.ui.annotations.ActionAnnotation import ActionAnnotation
from duit.ui.tk.TkFieldProperty import TkFieldProperty


class ActionProperty(TkFieldProperty[ActionAnnotation, DataField]):
    def __init__(self, annotation: ActionAnnotation, model: Optional[DataField] = None):
        """
        Initialize an ActionProperty.

        Args:
            annotation (ActionAnnotation): The ActionAnnotation associated with the property.
            model (Optional[DataField]): The model object for the property, if applicable.
        """
        super().__init__(annotation, model, hide_label=not annotation.show_label)

    def create_field(self, master) -> CTkBaseClass:
        """
        Create and return the GUI field for the action property.

        Args:
            master: The master widget where the field will be created.

        Returns:
            CTkBaseClass: The created GUI field.
        """
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
        """
        Run the action method associated with the property.
        """
        self.model.value()
