import gc

import nanogui
from nanogui import *
from nanogui import Screen, FormHelper

from Config import Config
from duit.ui.tk.TkPropertyPanel import TkPropertyPanel
from duit.ui.tk.TkPropertyRegistry import init_tk_registry


def main():
    nanogui.init()

    config = Config()
    screen = Screen((500, 700), "Configuration")

    gui = FormHelper(screen)
    window = gui.add_window((0, 0), "Form helper example")

    gui.add_group("Basic types")

    # panel.data_context = config

    def on_hungry(value):
        print(f"hungry changed to: {value}")

    config.hungry.on_changed += on_hungry

    screen.set_visible(True)
    screen.perform_layout()

    nanogui.mainloop()
    screen = gui = window = None
    gc.collect()
    nanogui.shutdown()


if __name__ == '__main__':
    main()
