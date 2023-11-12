from open3d.visualization import gui

from duit import ui
from duit.model.DataField import DataField
from duit.ui.ContainerHelper import ContainerHelper
from duit.ui.open3d.Open3dPropertyPanel import Open3dPropertyPanel
from duit.ui.open3d.Open3dPropertyRegistry import init_open3d_registry


class Config:
    def __init__(self):
        container_helper = ContainerHelper(self)

        with container_helper.section("Device"):
            self.device = DataField(0) | ui.Number("Device")
            self.write_output = DataField(False) | ui.Boolean("Write Output", readonly=True)

        # create section for debug parameters
        with container_helper.section("Debug"):
            self.debug_text = DataField("123") | ui.Text("Dbg", tooltip="The debug text.")
            self.threshold = DataField(127) | ui.Slider("Threshold", limit_min=0, limit_max=255)


def main():
    # create initial config
    config = Config()

    # create open3d gui for to display config
    init_open3d_registry()

    app = gui.Application.instance
    app.initialize()

    window: gui.Window = gui.Application.instance.create_window("Demo Window", 400, 200)
    panel = Open3dPropertyPanel(window)
    window.add_child(panel)
    panel.data_context = config

    app.run()


if __name__=="__main__":
    main()
