import argparse

from nicegui import ui

from duit.arguments.Arguments import Arguments
from duit.ui.nicegui.NiceGUIPropertyPanel import NiceGUIPropertyPanel
from duit.ui.nicegui.NiceGUIPropertyRegistry import init_nicegui_registry
from playground.Config import Config


def main():
    init_nicegui_registry()

    config = Config()
    config.age.value = 10

    arguments = Arguments()
    parser = argparse.ArgumentParser(description="Demo Project")
    args = arguments.add_and_configure(parser, config)

    def on_code_changed(index):
        print(config.codes[index])

    def on_hungry(value):
        print(f"hungry changed to: {value}")

    def on_resolution_changed(value):
        print(f"Resolution: {value}")

    config.hungry.on_changed += on_hungry
    config.resolution.on_changed += on_resolution_changed
    config.codes.on_index_changed += on_code_changed

    print(f"City: {config.location.value.city.value}")
    print(f"Library: {config.library.value}")

    # add panel
    panel = NiceGUIPropertyPanel().classes("w-full")
    panel.data_context = config

    ui.run(native=True, title="Demo Project", window_size=(500, 800), dark=True)


if __name__ in {"__main__", "__mp_main__"}:
    main()
