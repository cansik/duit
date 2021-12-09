from examples.Color import Color
from simbi.model.DataField import DataField
from simbi.ui.annotations import NumberAnnotation
from simbi.ui.annotations.ActionAnnotation import ActionAnnotation
from simbi.ui.annotations.BooleanAnnotation import BooleanAnnotation
from simbi.ui.annotations.EnumAnnotation import EnumAnnotation
from simbi.ui.annotations.OptionsAnnotation import OptionsAnnotation
from simbi.ui.annotations.SliderAnnotation import SliderAnnotation
from simbi.ui.annotations.TextAnnotation import TextAnnotation


class Config:
    def __init__(self):
        self.age = DataField(5) | NumberAnnotation("Age")
        self.hungry = DataField(True) | BooleanAnnotation("Hungry")
        self.year = DataField(2021) | NumberAnnotation("Year", 2000, 2050)
        self.temperature = DataField(30.2) | SliderAnnotation("Temperature", 0, 40)
        self.rings = DataField(30) | SliderAnnotation("Rings", 0, 40)

        self.resolution = DataField(256) | OptionsAnnotation("Resolution", [64, 128, 256, 512, 1024])
        self.color = DataField(Color.White) | EnumAnnotation("Color")

        self.name = DataField("Test") | TextAnnotation("Name", readonly=True)
        self._on_hello = DataField(self.say_hello) | ActionAnnotation("Press Me")

    def say_hello(self):
        print("hello world")
