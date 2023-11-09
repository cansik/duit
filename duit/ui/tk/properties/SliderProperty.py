import customtkinter as ctk
from customtkinter.windows.widgets.core_widget_classes import CTkBaseClass

from duit.model.DataField import DataField
from duit.ui.annotations.SliderAnnotation import SliderAnnotation
from duit.ui.tk.TkFieldProperty import TkFieldProperty
from duit.ui.tk.widgets.CTkNumberEntry import CTkNumberEntry


class SliderProperty(TkFieldProperty[SliderAnnotation, DataField]):
    def create_field(self, master) -> CTkBaseClass:
        """
        Create a slider field for the given slider annotation.

        Args:
            master: The parent widget.

        Returns:
            CTkBaseClass: The created slider field.
        """
        frame = ctk.CTkFrame(master, fg_color="transparent", corner_radius=0)
        frame.grid_columnconfigure(0, weight=1)

        data_variable = ctk.IntVar() if isinstance(self.model.value, int) else ctk.DoubleVar()
        field = ctk.CTkSlider(frame, variable=data_variable, from_=self.annotation.limit_min,
                              to=self.annotation.limit_max)
        field.grid(row=0, column=0, padx=5, pady=0, sticky="ew")

        number_entry = CTkNumberEntry(frame, self.model.value, self.annotation.limit_min, self.annotation.limit_max,
                                      width=80)
        number_entry.grid(row=0, column=1, padx=5, pady=0, sticky="nse")

        def on_dm_changed(value):
            data_variable.set(value)
            number_entry.value = value

        def on_ui_changed(event):
            self.model.value = data_variable.get()

        def on_entry_changed(event):
            self.model.value = number_entry.value

        self.model.on_changed.append(on_dm_changed)
        field.configure(command=on_ui_changed)
        number_entry.on_changed(on_entry_changed)

        self.model.fire_latest()

        return frame
