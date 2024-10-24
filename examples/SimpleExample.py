import argparse

from open3d.visualization import gui

from duit import ui
from duit.arguments.Argument import Argument
from duit.arguments.Arguments import DefaultArguments
from duit.model.DataField import DataField
from duit.settings.Settings import DefaultSettings
from duit.ui.ContainerHelper import ContainerHelper
from duit.ui.open3d.Open3dPropertyPanel import Open3dPropertyPanel
from duit.ui.open3d.Open3dPropertyRegistry import init_open3d_registry


class Config:
    def __init__(self):
        container_helper = ContainerHelper(self)

        with container_helper.section("User"):
            self.name = DataField("Cat") | ui.Text("Name")
            self.age = DataField(21) | ui.Slider("Age", limit_min=18, limit_max=99)

        with container_helper.section("Application"):
            self.enabled = DataField(True) | ui.Boolean("Enabled") | Argument()


def main():
    # create initial config
    config = Config()

    # register a custom listener for the enabled flag
    config.enabled.on_changed += lambda e: print(f"Enabled: {e}")

    # add arguments and parse
    parser = argparse.ArgumentParser()
    args = DefaultArguments.add_and_configure(parser, config)

    # store current config
    DefaultSettings.save("config.json", config)

    # create open3d gui for to display config
    init_open3d_registry()

    app = gui.Application.instance
    app.initialize()

    window: gui.Window = gui.Application.instance.create_window("Demo Window", 400, 200)
    panel = Open3dPropertyPanel(window)
    window.add_child(panel)
    panel.data_context = config

    app.run()


if __name__ == "__main__":
    main()
