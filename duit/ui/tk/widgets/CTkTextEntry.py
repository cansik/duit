import customtkinter
from customtkinter import CTkEntry


class CTkTextEntry(CTkEntry):
    def __init__(self, master: any, **kwargs):
        """
        Initialize a CTkTextEntry instance, which is a custom text entry field.

        Args:
            master (any): The parent widget.
            **kwargs: Additional keyword arguments for the CTkEntry constructor.
        """
        super().__init__(master, **kwargs)
        self._variable = customtkinter.StringVar()
        self.configure(textvariable=self._variable)
        self._readonly = False

    @property
    def readonly(self) -> bool:
        """
        Get the read-only status of the text entry.

        Returns:
            bool: True if the text entry is read-only, otherwise False.
        """
        return self._readonly

    @readonly.setter
    def readonly(self, value: bool):
        """
        Set the read-only status of the text entry.

        Args:
            value (bool): True to set the text entry as read-only, False to make it editable.
        """
        self._readonly = value
        if value:
            self.configure(state="readonly")
        else:
            self.configure(state="normal")

    @property
    def text(self) -> str:
        """
        Get the text content of the text entry.

        Returns:
            str: The text content of the text entry.
        """
        return self._variable.get()

    @text.setter
    def text(self, text: str):
        """
        Set the text content of the text entry.

        Args:
            text (str): The text content to set.
        """
        self._variable.set(text)

    def on_changed(self, callback):
        """
        Bind a callback function to the text entry's focus out event.

        Args:
            callback: The callback function to be called when the focus out event is triggered.
        """
        self.bind("<FocusOut>", callback)
