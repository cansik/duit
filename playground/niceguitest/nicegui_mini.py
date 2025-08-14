from nicegui import ui


def main():
    ui.label('Hello NiceGUI!')

    print("pre-run")
    ui.run(native=True, reload=False)
    print("post-run")


# if __name__ in {"__main__", "__mp_main__"}:
if __name__ == "__main__":
    main()
