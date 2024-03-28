import random
from pathlib import Path

import vector

import duit.ui as ui
from duit.annotation.AnnotationList import AnnotationList
from duit.arguments.Argument import Argument
from duit.model.DataField import DataField
from duit.model.SelectableDataList import SelectableDataList
from duit.settings.Setting import Setting
from duit.ui.annotations.PathAnnotation import DialogType
from playground.Color import Color
from playground.SubConfig import SubConfig


class Config:
    def __init__(self):
        self.is_active = DataField(False) | ui.Boolean("Active")

        self.age = DataField(5) | AnnotationList(
            ui.StartSection("Options", collapsed=False, is_active_field=self.is_active), ui.Number("Age"))
        self.hungry = DataField(True) | ui.Boolean("Hungry") | Setting(exposed=False)
        self.year = DataField(2021) | ui.Number("Year", 2000, 2050)
        self.humidity = DataField(18.5) | ui.Number("Humidity", readonly=True)
        self.humidity2 = DataField(18.5) | ui.Number("Humidity 2")
        self.temperature = DataField(30.2) | ui.Slider("Temperature", 0, 40)
        self.progress = DataField(0.75) | ui.Progress("A very\nlong label")
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
