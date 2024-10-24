from customtkinter.windows.widgets.core_widget_classes import CTkBaseClass

from duit.model.DataField import DataField
from duit.ui.annotations import NumberAnnotation
from duit.ui.tk.TkFieldProperty import TkFieldProperty
from duit.ui.tk.widgets.CTkNumberEntry import CTkNumberEntry


class NumberProperty(TkFieldProperty[NumberAnnotation, DataField]):
    """
    Property class for handling number-based fields in a Tkinter-based UI.

    This property displays a number field in a Tkinter UI, allowing the user to input numerical values within specified limits.

    Attributes:
        annotation (NumberAnnotation): The annotation for this property.
        model (DataField, optional): The data model associated with this property.
    """

    def create_field(self, master) -> CTkBaseClass:
        """
        Create the number field widget for the property.

        Args:
            master: The master widget or frame to which the number field widget is added.

        Returns:
            CTkBaseClass: The created number field widget.
        """
        field = CTkNumberEntry(master,
                               self.model.value,
                               self.annotation.limit_min,
                               self.annotation.limit_max,
                               self.annotation.decimal_precision)

        def on_dm_changed(value):
            field.value = value

        def on_ui_changed(event):
            value = field.value

            if value is None:
                self.model.fire()
                return

            self.model.value = value

        self.model.on_changed.append(on_dm_changed)
        field.on_changed(on_ui_changed)

        self.model.fire_latest()

        return field
