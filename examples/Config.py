from simbi.model.DataModel import DataModel
from simbi.ui.annotations import NumberAnnotation
from simbi.ui.annotations.BooleanAnnotation import BooleanAnnotation
from simbi.ui.annotations.OptionsAnnotation import OptionsAnnotation
from simbi.ui.annotations.SliderAnnotation import SliderAnnotation


class Config:
    def __init__(self):
        self.age = DataModel(5) | NumberAnnotation("Age")
        self.hungry = DataModel(True) | BooleanAnnotation("Hungry")
        self.year = DataModel(2021) | NumberAnnotation("Year", 2000, 2050)
        self.temperature = DataModel(30.2) | SliderAnnotation("Temperature", 0, 40)

        self.resolution = DataModel(256) | OptionsAnnotation("Resolution", [64, 128, 256, 512, 1024])
