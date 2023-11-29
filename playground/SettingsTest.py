from duit.model.DataField import DataField
from duit.settings.Setting import Setting
from duit.settings.Settings import DefaultSettings


class Config:
    def __init__(self):
        self.a = DataField("A")
        self.b = DataField("B") | Setting(name="b-field", load_order=5, save_order=10)
        self.c = DataField("C") | Setting(load_order=1)


def main():
    settings_path = "settings-test.json"
    config = Config()

    # store default
    DefaultSettings.save(settings_path, config)

    # change values
    config.a.value = "a"
    config.b.value = "b"
    config.c.value = "c"

    config.a.on_changed += lambda x: print(f"A changed: {x}")
    config.b.on_changed += lambda x: print(f"B changed: {x}")
    config.c.on_changed += lambda x: print(f"C changed: {x}")

    DefaultSettings.load(settings_path, config)

    print(config.a)
    print(config.b)
    print(config.c)


if __name__ == "__main__":
    main()
