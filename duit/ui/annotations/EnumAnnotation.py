from duit.ui.annotations.OptionsAnnotation import OptionsAnnotation


class EnumAnnotation(OptionsAnnotation):
    def __init__(self, name: str, tooltip: str = "", readonly: bool = False):
        super().__init__(name, [], tooltip, readonly)
