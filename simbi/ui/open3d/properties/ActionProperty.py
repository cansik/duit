import threading
from typing import Optional

from open3d.cpu.pybind.visualization.gui import Widget
from open3d.visualization import gui

from simbi.model.DataField import DataField
from simbi.ui.annotations.ActionAnnotation import ActionAnnotation
from simbi.ui.open3d.Open3dFieldProperty import Open3dFieldProperty


class ActionProperty(Open3dFieldProperty[ActionAnnotation]):
    def __init__(self, annotation: ActionAnnotation, model: Optional[DataField] = None):
        super().__init__(annotation, model, hide_label=not annotation.show_label)

    def create_field(self) -> Widget:
        field = gui.Button(self.annotation.text)
        field.horizontal_padding_em = 0.1
        field.vertical_padding_em = 0.1

        def on_clicked():
            if self.model is None:
                return

            if self.annotation.threaded:
                thread = threading.Thread(target=self._run_method, daemon = True)
                thread.start()
            else:
                self._run_method()

        field.set_on_clicked(on_clicked)
        return field

    def _run_method(self):
        self.model.value()
