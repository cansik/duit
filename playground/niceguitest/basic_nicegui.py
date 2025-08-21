import gc
import multiprocessing
import random
import threading
import time

from nicegui import ui, app

from duit import ui as dui
from duit.model.DataField import DataField
from duit.ui.ContainerHelper import ContainerHelper
from duit.ui.nicegui.NiceGUIPropertyPanel import NiceGUIPropertyPanel
from duit.ui.nicegui.NiceGUIPropertyRegistry import init_nicegui_registry
from duit.utils import macos_utils


def info(sender: str):
    print(
        f"{sender}: {threading.current_thread().name} ({threading.current_thread().native_id}) / {multiprocessing.current_process().name} ({multiprocessing.current_process().pid})")


class MySubConfig:
    def __init__(self):
        self.sub_text = DataField("Sub Text") | dui.Text("Sub Text")


class BasicConfig:
    def __init__(self):
        container_helper = ContainerHelper(self)

        self.first = DataField("First") | dui.Text("First")

        with container_helper.section("Section"):
            self.second = DataField("Second") | dui.Text("Second")
            self.nested_sub = DataField(MySubConfig()) | dui.SubSection("Nested Sub")
            self.really = DataField(False) | dui.Boolean("Really")

        self.after = DataField("After") | dui.Text("After")

        self.sub = DataField(MySubConfig()) | dui.SubSection("Sub")
        self.last = DataField("Last") | dui.Text("Last")


def main():
    init_nicegui_registry()

    config = BasicConfig()

    # add panel to main page
    @ui.page("/")
    def index_page():
        panel = NiceGUIPropertyPanel().classes("w-full")
        panel.data_context = config

        # remove padding
        ui.query('.nicegui-content').classes('p-1')

    def loop():
        while True:
            on = random.uniform(0, 1) > 0.5
            config.really.value = on

            time.sleep(random.uniform(0, 5))

            if random.uniform(0, 1) > 0.5:
                gc.collect()

    t = threading.Thread(target=loop, daemon=True)
    t.start()

    @app.on_startup
    def startup():
        info("startup")

    @app.on_connect
    def connect():
        info("connect")

    info("pre")
    ui.run(native=True, title="Basic Config", window_size=(500, 800), dark=False, reload=False)

    info("post")


# this is called on start
if __name__ == "__main__":
    main()

# this is called when the native window is run
if __name__ == "__mp_main__":
    info("mp_main")
    macos_utils.set_app_icon("icon.png")


    def window_opened():
        info("window_opened")
        macos_utils.set_dock_badge_label("👾")


    win = app.native.start_args["func"] = window_opened
