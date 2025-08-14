from dataclasses import dataclass
from typing import Callable, Any, Dict, List, get_type_hints


class ObservableMeta(type):
    def __new__(mcls, name, bases, ns):
        cls = super().__new__(mcls, name, bases, ns)

        # Find dataclass fields from annotations
        try:
            hints = get_type_hints(cls, include_extras=True)
        except Exception:
            hints = ns.get("__annotations__", {}) or {}

        fields = list(hints.keys())

        # Generate on_<field>_changed(self, callback) methods
        for field in fields:
            method_name = f"on_{field}_changed"
            if not hasattr(cls, method_name):
                def make_register(fname: str):
                    def register(self, callback: Callable[[Any, Any], None]):
                        # Store callbacks under fname and return the callback for decorator use
                        self._observers.setdefault(fname, []).append(callback)
                        return callback

                    register.__name__ = method_name
                    register.__doc__ = f"Register a callback for changes to {field}."
                    return register

                setattr(cls, method_name, make_register(field))

        return cls


class Observable(metaclass=ObservableMeta):
    _observers: Dict[str, List[Callable[[Any, Any], None]]]

    def __setattr__(self, key, value):
        # Read old value if present
        has_old = hasattr(self, key)
        old = object.__getattribute__(self, key) if has_old else None

        # Set first so the object state is consistent for callbacks
        super().__setattr__(key, value)

        # No callbacks during __init__ before _observers exists
        obs = self.__dict__.get("_observers")
        if not obs:
            return

        # Fire callbacks if any were registered for this key
        for cb in obs.get(key, []):
            cb(old, value)

    def __post_init__(self):
        # Created after dataclass sets fields so init does not fire callbacks
        object.__setattr__(self, "_observers", {})


@dataclass
class Config(Observable):
    name: str = "Amy"
    age: int = 78


def main():
    c = Config()

    # As a normal call
    def name_logger(old, new):
        print(f"name changed from {old} to {new}")

    c.on_name_changed(name_logger)

    # As a decorator
    @c.on_age_changed
    def age_logger(old, new):
        print(f"age changed from {old} to {new}")

    print("initial:", c.name, c.age)
    c.name = "Olaf"
    c.age = 79


if __name__ == "__main__":
    main()
