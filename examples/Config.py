from examples.Color import Color
from examples.SubConfig import SubConfig
from simbi.model.DataField import DataField
import simbi.ui as ui


class Config:
    def __init__(self):
        self.age = DataField(5) | ui.StartSection("Options", collapsed=True) | ui.Number("Age")
        self.hungry = DataField(True) | ui.Boolean("Hungry")
        self.year = DataField(2021) | ui.Number("Year", 2000, 2050)
        self.temperature = DataField(30.2) | ui.Slider("Temperature", 0, 40)
        self.rings = DataField(30) | ui.EndSection() | ui.Slider("Rings", 0, 40)

        self.resolution = DataField(256) | ui.Options("Resolution", [64, 128, 256, 512, 1024])
        self.color = DataField(Color.White) | ui.Enum("Color")

        self.name = DataField("Test") | ui.Text("Name", readonly=True)
        self._on_hello = DataField(self.say_hello) | ui.Action("Press Me")

        self.location = DataField(SubConfig())

    def say_hello(self):
        print("hello world")
