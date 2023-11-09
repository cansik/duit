from duit.ui.annotations.UIAnnotation import UIAnnotation


class ProgressAnnotation(UIAnnotation):
    def __init__(self, name: str, tooltip: str = ""):
        """
        Initialize a ProgressAnnotation.

        :param name: The name of the progress annotation.
        :param tooltip: The tooltip text for the annotation.
        """
        super().__init__(name, tooltip)
