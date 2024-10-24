import argparse
from typing import Any

from duit.arguments.Argument import Argument
from duit.arguments.adapters.BaseTypeAdapter import BaseTypeAdapter


class DefaultTypeAdapter(BaseTypeAdapter):
    """
    A default type adapter for command-line arguments.

    Attributes:
        None
    """

    def handles_type(self, obj: Any) -> bool:
        """
        Check if the type adapter can handle a specific data type.

        Args:
            obj (Any): The data type to be checked.

        Returns:
            bool: Always returns True, as the default type adapter handles any data type.
        """
        return True

    def add_argument(self, parser, argument: Argument, obj: Any):
        """
        Add a command-line argument to an argparse parser based on the default type adapter.

        Args:
            parser (argparse.ArgumentParser): The argparse parser to which the argument will be added.
            argument (Argument): The Argument annotation associated with the argument.
            obj (Any): The value of the argument.

        Returns:
            None
        """
        parser.add_argument(argument.dest, *argument.args, **argument.kwargs)

    def parse_argument(self, args: argparse.Namespace, ns_dest: str, argument: Argument, obj: Any) -> Any:
        """
        Parse a command-line argument value from argparse namespace and return it based on the default type adapter.

        Args:
            args (argparse.Namespace): The argparse namespace containing the parsed command-line arguments.
            ns_dest (str): The namespace attribute name of the argument.
            argument (Argument): The Argument annotation associated with the argument.
            obj (Any): The original value of the argument.

        Returns:
            Any: The parsed value of the argument.
        """
        return getattr(args, ns_dest)
