from duit.model.DataField import DataField
import duit.ui as ui


class SubConfig:
    def __init__(self):
        self.city = DataField("Berlin") | ui.Text("City")
