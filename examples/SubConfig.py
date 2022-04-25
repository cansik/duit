from simbi.model.DataField import DataField
import simbi.ui as ui


class SubConfig:
    def __init__(self):
        self.city = DataField("Berlin") | ui.Number("City")
