import argparse
from abc import ABC, abstractmethod
from typing import Any

from duit.arguments.Argument import Argument


class BaseTypeAdapter(ABC):
    """
    An abstract base class for defining type adapters for command-line arguments.

    Attributes:
        None
    """

    @abstractmethod
    def handles_type(self, obj: Any) -> bool:
        """
        Check if the type adapter can handle a specific data type.

        Args:
            obj (Any): The data type to be checked.

        Returns:
            bool: True if the type adapter can handle the data type, False otherwise.
        """
        pass

    @abstractmethod
    def add_argument(self, parser, argument: Argument, obj: Any):
        """
        Add a command-line argument to an argparse parser based on the type adapter.

        Args:
            parser (argparse.ArgumentParser): The argparse parser to which the argument will be added.
            argument (Argument): The Argument annotation associated with the argument.
            obj (Any): The value of the argument.

        Returns:
            None
        """
        pass

    @abstractmethod
    def parse_argument(self, args: argparse.Namespace, ns_dest: str, argument: Argument, obj: Any) -> Any:
        """
        Parse a command-line argument value from argparse namespace and return it based on the type adapter.

        Args:
            args (argparse.Namespace): The argparse namespace containing the parsed command-line arguments.
            ns_dest (str): The namespace attribute name of the argument.
            argument (Argument): The Argument annotation associated with the argument.
            obj (Any): The original value of the argument.

        Returns:
            Any: The parsed value of the argument.
        """
        pass
