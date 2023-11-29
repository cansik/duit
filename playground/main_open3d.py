import argparse

import open3d as o3d

from Config import Config
from DemoWindow import DemoWindow
from duit.arguments.Arguments import Arguments
from duit.settings.Settings import Settings
from duit.ui.open3d.Open3dPropertyRegistry import init_open3d_registry


def main():
    init_open3d_registry()

    config = Config()
    config.age.value = 10

    arguments = Arguments()
    parser = argparse.ArgumentParser(description="Demo Project")
    args = arguments.add_and_configure(parser, config)

    settings = Settings()
    settings.save("test.json", config)
    settings.load("test.json", config)

    def on_code_changed(index):
        print(config.codes[index])

    config.codes.on_index_changed += on_code_changed

    print(f"City: {config.location.value.city.value}")
    print(f"Library: {config.library.value}")

    app = o3d.visualization.gui.Application.instance
    app.initialize()

    win = DemoWindow(config)

    app.run()


if __name__ == '__main__':
    main()
