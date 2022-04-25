from duit.ui.annotations.OptionsAnnotation import OptionsAnnotation


class EnumAnnotation(OptionsAnnotation):
    def __init__(self, name: str, readonly: bool = False):
        super().__init__(name, [], readonly)
