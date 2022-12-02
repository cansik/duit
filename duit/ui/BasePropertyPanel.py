from abc import ABC, abstractmethod
from typing import Optional, Any


class BasePropertyPanel(ABC):
    def __init__(self):
        self._data_context: Optional[Any] = None

    @property
    def data_context(self):
        return self._data_context

    @data_context.setter
    def data_context(self, value):
        self._data_context = value
        self._create_panel()

    @abstractmethod
    def _create_panel(self):
        pass
