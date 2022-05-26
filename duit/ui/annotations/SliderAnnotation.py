from duit.ui.annotations import NumberAnnotation


class SliderAnnotation(NumberAnnotation):
    def __init__(self, name: str, limit_min: float = 0, limit_max: float = 1,
                 tooltip: str = "", readonly: bool = False):
        super().__init__(name, limit_min, limit_max, 3, tooltip, readonly)
