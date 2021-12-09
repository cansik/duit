from simbi.ui.annotations import NumberAnnotation


class SliderAnnotation(NumberAnnotation):
    def __init__(self, name: str, limit_min: float = 0, limit_max: float = 1):
        super().__init__(name, limit_min, limit_max)
