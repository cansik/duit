import threading
from typing import Optional

from open3d.cpu.pybind.visualization.gui import Widget
from open3d.visualization import gui

from duit.model.DataField import DataField
from duit.ui.annotations.ActionAnnotation import ActionAnnotation
from duit.ui.open3d import Open3dContext
from duit.ui.open3d.Open3dFieldProperty import Open3dFieldProperty


class ActionProperty(Open3dFieldProperty[ActionAnnotation, DataField]):
    def __init__(self, annotation: ActionAnnotation, model: Optional[DataField] = None):
        """
        Initialize an ActionProperty.

        :param annotation: The ActionAnnotation associated with this property.
        :param model: The data model for this property (default is None).
        """
        super().__init__(annotation, model, hide_label=not annotation.show_label)

    def create_field(self) -> Widget:
        """
        Create the field widget for the ActionProperty.

        This method generates a button widget for the ActionProperty.

        :return: The button widget.
        """
        field = gui.Button(self.annotation.text)
        field.horizontal_padding_em = 0.01 * Open3dContext.OPEN3D_FONT_EM
        field.vertical_padding_em = 0.01 * Open3dContext.OPEN3D_FONT_EM
        field.tooltip = self.annotation.tooltip

        def on_clicked():
            if self.model is None:
                return

            if self.annotation.threaded:
                thread = threading.Thread(target=self._run_method, daemon=True)
                thread.start()
            else:
                self._run_method()

        field.set_on_clicked(on_clicked)
        return field

    def _run_method(self):
        """
        Run the action method associated with the ActionProperty.

        This method is called when the button widget is clicked. It executes the action method associated with the
        property's data model.
        """
        self.model.value()
