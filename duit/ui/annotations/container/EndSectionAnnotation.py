from duit.ui.annotations import UIAnnotation


class EndSectionAnnotation(UIAnnotation):
    def __init__(self):
        super().__init__("", importance=15)
