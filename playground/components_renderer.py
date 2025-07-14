# pip install mss

import asyncio
import sys
from enum import Enum
from pathlib import Path

import mss.tools as mss_tools
import vector
from mss import mss
from nicegui import ui, app

from duit import ui as dui
from duit.model.DataField import DataField
from duit.model.SelectableDataList import SelectableDataList
from duit.ui.annotations.PathAnnotation import DialogType
from duit.ui.nicegui.NiceGUIPropertyPanel import NiceGUIPropertyPanel
from duit.ui.nicegui.NiceGUIPropertyRegistry import init_nicegui_registry
from playground import quartz_window


class RenderConfig:
    def __init__(self, *fields: DataField):
        for i, field in enumerate(fields):
            self.__setattr__(f"field_{i:04d}", field)


class Color(Enum):
    Red = 0
    Green = 1
    Blue = 2


components = {
    "Number": DataField(4) | dui.Number("Count", limit_min=0, limit_max=10),
    "Slider": DataField(0.5) | dui.Slider("Opacity", limit_min=0, limit_max=1),
    "Boolean": DataField(True) | dui.Boolean("Enabled"),
    "Text": DataField("Hello") | dui.Text("Message", placeholder_text="enter text"),
    "Options": DataField("auto") | dui.Options("Mode", ["auto", "manual"]),
    "Enum": DataField(Color.Red) | dui.Enum("Color"),
    "Vector2": DataField(vector.obj(x=5.0, y=0.3)) | dui.Vector("Position"),
    "Vector3": DataField(vector.obj(x=5.0, y=0.3, z=1)) | dui.Vector("Velocity"),
    "Vector4": DataField(vector.obj(x=5.0, y=0.3, z=1, t=0.5)) | dui.Vector("Acceleration"),
    "List": SelectableDataList([1, 2, 3]) | dui.List("Items"),
    "Path": DataField(Path("test.json")) | dui.Path("Output", dialog_type=DialogType.SaveFile),
    "Progress": DataField(0.5) | dui.Progress("Loading"),
    "Action": DataField(None) | dui.Action("Press Me"),
    "Title": DataField("Content") | dui.Title(text_color=(255, 255, 0))
}


def main():
    window_title = "DuitComponentsRenderer"
    output_path = Path("doc/components/")
    output_path.mkdir(exist_ok=True, parents=True)

    init_nicegui_registry()

    @ui.page("/")
    def index_page():
        panel = NiceGUIPropertyPanel().classes("w-full")
        panel.data_context = RenderConfig()

        async def on_connect():
            for key in components.keys():
                print(f"displaying {key}")
                panel.data_context = RenderConfig(components[key])
                await asyncio.sleep(0.5)

                # grab the first match
                win = quartz_window.get_foremost_window_bounds(include_border=False)

                # get its geometry
                left, top = win["x"], win["y"]
                width, height = win["width"], win["height"]

                with mss() as sct:
                    monitor = {
                        "left": left,
                        "top": top,
                        "width": width,
                        "height": height,
                    }
                    img = sct.grab(monitor)

                    # save to file
                    mss_tools.to_png(img.rgb, img.size, output=str(output_path / f"{key}Component.png"), level=1)

                await asyncio.sleep(0.2)
            sys.exit()

        app.on_connect(on_connect)

    ui.run(native=True, title=window_title, window_size=(500, 100), dark=True, reload=False)


if __name__ in {"__main__", "__mp_main__"}:
    main()
