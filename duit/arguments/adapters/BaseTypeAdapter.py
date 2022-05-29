import argparse
from abc import ABC, abstractmethod
from typing import Any, Type

from duit.arguments.Argument import Argument


class BaseTypeAdapter(ABC):

    @abstractmethod
    def handles_type(self, obj: Any) -> bool:
        pass

    @abstractmethod
    def add_argument(self, parser, argument: Argument, data_type: Type) -> Argument:
        pass

    @abstractmethod
    def parse_argument(self, args: argparse.Namespace, dest: str, argument: Argument, data_type: Type) -> Any:
        pass
