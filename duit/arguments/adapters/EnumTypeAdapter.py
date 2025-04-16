import argparse
from enum import Enum
from typing import Any, Optional

from duit.arguments.Argument import Argument
from duit.arguments.adapters.BaseTypeAdapter import BaseTypeAdapter


class EnumTypeAdapter(BaseTypeAdapter):
    """
    A type adapter for handling command-line arguments of enum types.

    Attributes:
        None
    """

    def handles_type(self, obj: Any) -> bool:
        """
        Check if the type adapter can handle a specific data type (enum).

        Args:
            obj (Any): The data type to be checked.

        Returns:
            bool: True if the type adapter can handle enum data types, False otherwise.
        """
        return isinstance(obj, Enum)

    def add_argument(self, parser, argument: Argument, obj: Enum):
        """
        Add a command-line argument to an argparse parser based on the Enum type adapter.

        Args:
            parser (argparse.ArgumentParser): The argparse parser to which the argument will be added.
            argument (Argument): The Argument annotation associated with the argument.
            obj (Enum): The enum type for which the argument is defined.

        Returns:
            None
        """
        items = {item.name: item for item in list(type(obj))}
        default_value: Optional[Enum] = argument.kwargs.get("default", None)

        argument.kwargs["default"] = default_value.name if default_value is not None else default_value
        argument.kwargs["metavar"] = ", ".join([v for v in items.keys()])
        argument.kwargs["type"] = str

        parser.add_argument(argument.dest, *argument.args, **argument.kwargs)

    def parse_argument(self, args: argparse.Namespace, ns_dest: str, argument: Argument, obj: Any) -> Any:
        """
        Parse a command-line argument value from argparse namespace and return the corresponding enum value.

        Args:
            args (argparse.Namespace): The argparse namespace containing the parsed command-line arguments.
            ns_dest (str): The namespace attribute name of the argument.
            argument (Argument): The Argument annotation associated with the argument.
            obj (Enum): The original enum type for which the argument is defined.

        Returns:
            Any: The parsed enum value.
        """
        items = {item.name: item for item in list(type(obj))}
        raw_value = getattr(args, ns_dest)

        return items[raw_value]
