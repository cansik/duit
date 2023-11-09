from duit.ui.annotations.OptionsAnnotation import OptionsAnnotation


class EnumAnnotation(OptionsAnnotation):
    def __init__(self, name: str, tooltip: str = "", readonly: bool = False):
        """
        Initialize an EnumAnnotation.

        :param name: The name of the enum annotation.
        :param tooltip: The tooltip text for the annotation.
        :param readonly: Whether the annotation is read-only (default is False).
        """
        super().__init__(name, [], tooltip, readonly)
