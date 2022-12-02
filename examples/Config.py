import vector

from duit.annotation.AnnotationList import AnnotationList
from duit.arguments.Argument import Argument
from examples.Color import Color
from examples.SubConfig import SubConfig
from duit.model.DataField import DataField
import duit.ui as ui


class Config:
    def __init__(self):
        self.age = DataField(5) | AnnotationList(ui.StartSection("Options", collapsed=True),
                                                 ui.Number("Age"))
        self.hungry = DataField(True) | ui.Boolean("Hungry")
        self.year = DataField(2021) | ui.Number("Year", 2000, 2050)
        self.humidity = DataField(18.5) | ui.Number("Humidity", readonly=True)
        self.temperature = DataField(30.2) | ui.Slider("Temperature", 0, 40)
        self.rings = DataField(30) | ui.EndSection() | ui.Slider("Rings", 0, 40)

        self.resolution = DataField(256) | ui.Options("Resolution", [64, 128, 256, 512, 1024])
        self.color = DataField(Color.White) | ui.Enum("Color") | Argument()

        self.name1 = DataField("Test 1") | ui.Text("Name") | Argument()
        self.name2 = DataField("Test 2") | ui.Text("Name", readonly=True)
        self.name3 = DataField("Test 3") | ui.Text("Name", readonly=True, copy_content=True)
        self._on_hello = DataField(self.say_hello) | ui.Action("Press Me")

        self.location = DataField(SubConfig()) | ui.SubSection("Location")
        self.library = DataField({"Book": "Test", "Movie": "World"})

    @staticmethod
    def say_hello():
        print("hello world")
