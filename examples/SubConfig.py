import vector

from duit.arguments.Argument import Argument
from duit.model.DataField import DataField
import duit.ui as ui


class SubConfig:
    def __init__(self):
        self.city = DataField("Berlin") | ui.Text("City", tooltip="City in Germany") | Argument()

        self.location2 = DataField(vector.obj(x=1.0, y=2.0)) | ui.Vector("Location 2", readonly=True, copy_content=True)
        self.location3 = DataField(vector.obj(x=1.0, y=2.0, z=5.0)) | ui.Vector("Location 3")
        self.location4 = DataField(vector.obj(x=1.0, y=2.0, z=5.0, t=2)) | ui.Vector("Location 4")

        self.city2 = DataField("Zurich") | ui.Text("City", tooltip="City in Switzerland")
