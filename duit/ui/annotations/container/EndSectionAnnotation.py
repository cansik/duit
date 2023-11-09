from duit.ui.annotations import UIAnnotation


class EndSectionAnnotation(UIAnnotation):
    def __init__(self):
        """
        Initialize an EndSectionAnnotation.

        This annotation is used to mark the end of a section in a user interface.

        """
        super().__init__("", importance=15)
