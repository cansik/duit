import argparse
from typing import Any

from duit.arguments.Argument import Argument
from duit.arguments.adapters.BaseTypeAdapter import BaseTypeAdapter


class BooleanTypeAdapter(BaseTypeAdapter):
    """
    A type adapter for handling command-line arguments of bool data type.
    """

    def handles_type(self, obj: Any) -> bool:
        """
        Check if the type adapter can handle a specific data type (bool).

        Args:
            obj (Any): The data type to be checked.

        Returns:
            bool: True if the type adapter can handle bool data types, False otherwise.
        """
        return isinstance(obj, bool)

    def add_argument(self, parser, argument: Argument, obj: Any):
        """
        Add a command-line argument to an argparse parser based on the bool type adapter.

        Args:
            parser (argparse.ArgumentParser): The argparse parser to which the argument will be added.
            argument (Argument): The Argument annotation associated with the argument.
            obj (Any): The value of the argument.

        Returns:
            None
        """

        # add action for boolean parameter
        kwargs = argument.kwargs
        if "action" not in kwargs:
            default_value = bool(kwargs.get("default", False))
            kwargs["action"] = "store_false" if default_value else "store_true"

        # remove type for action_class
        if "type" in kwargs:
            kwargs.pop("type")

        parser.add_argument(argument.dest, *argument.args, **argument.kwargs)

    def parse_argument(self, args: argparse.Namespace, ns_dest: str, argument: Argument, obj: Any) -> bool:
        """
        Parse a command-line argument value from argparse namespace and return it as a bool object.

        Args:
            args (argparse.Namespace): The argparse namespace containing the parsed command-line arguments.
            ns_dest (str): The namespace attribute name of the argument.
            argument (Argument): The Argument annotation associated with the argument.
            obj (Any): The original value of the argument.

        Returns:
            bool: The parsed bool object.
        """
        return bool(getattr(args, ns_dest))
