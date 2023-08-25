from Config import Config
from nicegui import ui


def main():
    config = Config()

    with ui.expansion('Expand!', icon='work').classes('w-full'):
        ui.label('Hello NiceGUI!')

    print(ui.expansion.value)

    ui.run()


if __name__ in ("__main__", "__mp_main__"):
    main()
