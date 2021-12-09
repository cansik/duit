from simbi.ui.annotations.OptionsAnnotation import OptionsAnnotation


class EnumAnnotation(OptionsAnnotation):
    def __init__(self, name: str):
        super().__init__(name, [])
