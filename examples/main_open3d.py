from Config import Config
import open3d as o3d
import argparse
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

    print(f"City: {config.location.value.city.value}")
    print(f"Library: {config.library.value}")

    app = o3d.visualization.gui.Application.instance
    app.initialize()

    win = DemoWindow(config)

    app.run()


if __name__ == '__main__':
    main()
