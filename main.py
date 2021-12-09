from Config import Config
import open3d as o3d
from DemoWindow import DemoWindow
from simbi.ui.open3d.Open3dPropertyRegistry import init_open3d_registry


def main():
    init_open3d_registry()

    config = Config()
    config.age.value = 10

    app = o3d.visualization.gui.Application.instance
    app.initialize()

    win = DemoWindow(config)

    app.run()


if __name__ == '__main__':
    main()
