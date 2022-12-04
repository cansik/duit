from customtkinter.windows.widgets.core_widget_classes import CTkBaseClass

from duit.ui.annotations import NumberAnnotation
from duit.ui.tk.TkFieldProperty import TkFieldProperty
from duit.ui.tk.widgets.CTkNumberEntry import CTkNumberEntry


class NumberProperty(TkFieldProperty[NumberAnnotation]):
    def create_field(self, master) -> CTkBaseClass:
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
