from duit.ui.annotations import UIAnnotation


class ActionAnnotation(UIAnnotation):
    def __init__(self, name: str, text: str = None, threaded: bool = True, show_label: bool = False):
        super().__init__(name)
        self.threaded = threaded
        self.text = text if text is not None else name
        self.show_label = show_label