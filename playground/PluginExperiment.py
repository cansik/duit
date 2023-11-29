from typing import Union

from duit.annotation.Annotation import Annotation, M
from duit.model.DataField import DataField
from duit.model.DataFieldPlugin import DataFieldPlugin

Number = Union[int, float]


class RangePlugin(DataFieldPlugin[Number]):

    def __init__(self, min_value: Number, max_value: Number):
        self.min_value = min_value
        self.max_value = max_value

    def on_set_value(self, field: DataField[Number], old_value: Number, new_value: Number) -> Number:
        return max(min(self.max_value, new_value), self.min_value)


class Range(Annotation):

    def __init__(self, min_value: Number, max_value: Number):
        self.min_value = min_value
        self.max_value = max_value

    def _apply_annotation(self, model: M) -> M:
        model.plugins.append(RangePlugin(self.min_value, self.max_value))
        return model

    @staticmethod
    def _get_annotation_attribute_name() -> str:
        return ""


def main():
    field = DataField(500) | Range(0, 1000)
    # field.plugins.append(RangePlugin(0, 1000))

    field.on_changed += lambda x: print(f"Value: {x}")

    field.value = 100
    field.value = 8000
    field.value = -50
    field.value = -0.23
    field.value = 20


if __name__ == "__main__":
    main()
