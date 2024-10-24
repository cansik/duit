from duit.ui.annotations.UIAnnotation import UIAnnotation


class TextAnnotation(UIAnnotation):
    def __init__(self, name: str, placeholder_text: str = "",
                 tooltip: str = "", readonly: bool = False, copy_content: bool = False):
        """
        Initialize a TextAnnotation.

        :param name: The name of the text annotation.
        :param placeholder_text: The placeholder text to display in the text field.
        :param tooltip: The tooltip text for the annotation.
        :param readonly: Whether the annotation is read-only (default is False).
        :param copy_content: Whether to enable content copying (default is False).
        """
        super().__init__(name, tooltip, readonly)
        self.placeholder_text = placeholder_text
        self.copy_content = copy_content
