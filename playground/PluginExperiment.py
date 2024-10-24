from typing import Union

from duit.annotation.Annotation import Annotation, M
from duit.model.DataField import DataField
from duit.model.DataFieldPlugin import DataFieldPlugin, T

Number = Union[int, float]


class RangePlugin(DataFieldPlugin[Number]):

    def __init__(self, min_value: Number, max_value: Number):
        super().__init__()
        self.min_value = min_value
        self.max_value = max_value

    def on_register(self, field: DataField[Number]):
        if not isinstance(field.value, Number.__args__):
            raise ValueError(f"Value of data-field {field} is not Number!")

    def on_set_value(self, field: DataField[Number], old_value: Number, new_value: Number) -> Number:
        return max(min(self.max_value, new_value), self.min_value)


class Range(Annotation):

    def __init__(self, min_value: Number, max_value: Number):
        self.min_value = min_value
        self.max_value = max_value

    def _apply_annotation(self, model: M) -> M:
        model.register_plugin(RangePlugin(self.min_value, self.max_value))
        return model

    @staticmethod
    def _get_annotation_attribute_name() -> str:
        return ""


def main():
    class TestPlugin(DataFieldPlugin):
        def on_get_value(self, _: DataField[T], value: T) -> T:
            return int(value)

        def on_set_value(self, _: DataField[T], old_value: T, new_value: T) -> T:
            return str(new_value)

    test_plugin = TestPlugin()
    test_plugin.order_index = -1

    field = DataField(500) | Range(0, 1000)
    field.register_plugin(test_plugin)
    # field.register_plugin(RangePlugin(0, 1000))

    field.on_changed += lambda x: print(f"Value: {x}")

    field.value = 100
    field.value = 8000
    field.value = -50
    field.value = -0.23
    field.value = 20

    print(field.plugins)


if __name__ == "__main__":
    main()
