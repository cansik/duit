import random
from pathlib import Path

import vector

from duit.annotation.AnnotationList import AnnotationList
from duit.arguments.Argument import Argument
from duit.model.DataList import DataList
from duit.model.SelectableDataList import SelectableDataList
from duit.ui.annotations.PathAnnotation import DialogType
from examples.Color import Color
from examples.SubConfig import SubConfig
from duit.model.DataField import DataField
import duit.ui as ui


class Config:
    def __init__(self):
        self.age = DataField(5) | AnnotationList(ui.StartSection("Options", collapsed=False), ui.Number("Age"))
        self.hungry = DataField(True) | ui.Boolean("Hungry")
        self.year = DataField(2021) | ui.Number("Year", 2000, 2050)
        self.humidity = DataField(18.5) | ui.Number("Humidity", readonly=True)
        self.temperature = DataField(30.2) | ui.Slider("Temperature", 0, 40)
        self.sunshine = DataField(0.5) | ui.Slider("Sunshine", 0, 1, show_number_field=False)
        self.rings = DataField(30) | ui.EndSection() | ui.Slider("Rings", 0, 40)
        self.speed = DataField(vector.obj(x=1.0, y=2.0)) | ui.Vector("Speed")
        self.velocity = DataField(vector.obj(x=1.0, y=2.0, z=5.0)) | ui.Vector("Velocity")

        self.resolution = DataField(256) | ui.Options("Resolution", [64, 128, 256, 512, 1024])
        self.color = DataField(Color.White) | ui.Enum("Color") | Argument()

        self.name1 = DataField("Test 1") | ui.Text("Name") | Argument()
        self.name2 = DataField("Test 2") | ui.Text("Name", readonly=True)
        self.name3 = DataField("Test 3") | ui.Text("Name", readonly=True, copy_content=True)

        self.home = DataField(Path()) | ui.Path("Home", dialog_type=DialogType.OpenDirectory) | Argument()
        self.main = DataField(Path()) | ui.Path("Main", filters={".py": "Python Files"})
        self.save = DataField(Path()) | ui.Path("Save", dialog_type=DialogType.SaveFile)

        self.check1 = DataField(False) | ui.Boolean("Check 1") | ui.StartSection("Boxes")
        self.check2 = DataField(False) | ui.Boolean("Check 2")
        self.check3 = DataField(False) | ui.Boolean("Check 3") | ui.EndSection()

        self._on_hello = DataField(self.say_hello) | ui.Action("Press Me")

        self.location = DataField(SubConfig()) | ui.SubSection("Location")
        self.library = DataField({"Book": "Test", "Movie": "World"})

        self.codes = SelectableDataList() | ui.List("Codes")

    def say_hello(self):
        print("hello world")
        self.codes.append(random.randint(0, 100))
