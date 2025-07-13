from nicegui import ui

from duit import ui as dui
from duit.model.DataField import DataField
from duit.ui.ContainerHelper import ContainerHelper
from duit.ui.nicegui.NiceGUIPropertyPanel import NiceGUIPropertyPanel
from duit.ui.nicegui.NiceGUIPropertyRegistry import init_nicegui_registry


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

    ui.run(native=True, title="Basic Config", window_size=(500, 800), dark=False, reload=False)


if __name__ in {"__main__", "__mp_main__"}:
    main()
