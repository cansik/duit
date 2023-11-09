from abc import ABC, abstractmethod
from typing import Optional, Any


class BasePropertyPanel(ABC):
    def __init__(self):
        """
        Initialize a BasePropertyPanel.

        The BasePropertyPanel is an abstract base class for panels that display
        properties. The `data_context` property can be used to set the data context
        for the panel.

        """
        self._data_context: Optional[Any] = None

    @property
    def data_context(self):
        """
        Get the data context for the panel.

        :return: The data context object associated with the panel.
        """
        return self._data_context

    @data_context.setter
    def data_context(self, value):
        """
        Set the data context for the panel.

        This method sets the data context for the panel and calls the `_create_panel`
        method to create the panel's contents based on the new data context.

        :param value: The data context object to set.
        """
        self._data_context = value
        self._create_panel()

    @abstractmethod
    def _create_panel(self):
        """
        Create the panel's contents.

        This method should be implemented by subclasses to create and define the
        content of the panel based on the current data context.

        """
        pass
