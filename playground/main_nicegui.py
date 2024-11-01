import threading
import time
from multiprocessing import Queue

from nicegui import ui, app
from nicegui.events import ValueChangeEventArguments

from Config import Config


def main():
    counter_queue = Queue()
    config = Config()

    with ui.expansion('Expand!', icon='work', value=True).classes('w-full'):
        ui.label('Hello NiceGUI!')
        with ui.row().__enter__() as r:
            def update_ui(e: ValueChangeEventArguments):
                config.age.value = e.value

            number = ui.number("Age:", value=config.age.value, on_change=update_ui)

            @config.age.on_changed.register
            def update_df(value):
                print(f"updated value to: {value}")
                number.value = value

            config.age.on_changed += update_df

    def update():
        config.age.value += 1
        time.sleep(1.0)

    threading.Thread(target=update, daemon=True).start()

    app.native.start_args['debug'] = True
    ui.run(native=True, window_size=(400, 300), fullscreen=False)


if __name__ in ("__main__", "__mp_main__"):
    main()
