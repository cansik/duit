from duit.ui.annotations import UIAnnotation


class ActionAnnotation(UIAnnotation):
    def __init__(self, name: str, text: str = None, threaded: bool = True, show_label: bool = False, tooltip: str = ""):
        """
        Initialize an ActionAnnotation.

        :param name: The name of the action.
        :param text: The text to display for the action (defaults to the name if not provided).
        :param threaded: Whether the action should be executed in a separate thread.
        :param show_label: Whether to show a label for the action.
        :param tooltip: The tooltip text for the action.
        """
        super().__init__(name, tooltip)
        self.threaded = threaded
        self.text = text if text is not None else name
        self.show_label = show_label
