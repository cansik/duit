from duit.ui.annotations import UIAnnotation


class SubSectionAnnotation(UIAnnotation):
    def __init__(self, name: str, collapsed: bool = False):
        super().__init__(name)
        self.collapsed = collapsed
