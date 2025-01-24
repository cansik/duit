import argparse
from typing import Any, Optional

import vector

from duit.arguments.Argument import Argument
from duit.arguments.adapters.BaseTypeAdapter import BaseTypeAdapter
from duit.utils import _vector


class VectorTypeAdapter(BaseTypeAdapter):
    """
    A type adapter for handling command-line arguments of vector.Vector data type.

    Attributes:
        None
    """

    def handles_type(self, obj: Any) -> bool:
        """
        Check if the type adapter can handle a specific data type (vector.Vector).

        Args:
            obj (Any): The data type to be checked.

        Returns:
            bool: True if the type adapter can handle vector.Vector data types, False otherwise.
        """
        return isinstance(obj, vector.Vector)

    def add_argument(self, parser, argument: Argument, obj: Any):
        """
        Add a command-line argument to an argparse parser based on the Vector type adapter.

        Args:
            parser (argparse.ArgumentParser): The argparse parser to which the argument will be added.
            argument (Argument): The Argument annotation associated with the argument.
            obj (Any): The value of the argument.

        Returns:
            None
        """
        components = _vector.get_vector_attributes(obj)
        default_value: Optional[vector.Vector] = argument.kwargs.get("default", None)

        argument.kwargs["metavar"] = components
        argument.kwargs["type"] = float
        argument.kwargs["nargs"] = len(components)
        argument.kwargs["default"] = [getattr(default_value, c)
                                      for c in components] if default_value is not None else None

        parser.add_argument(argument.dest, *argument.args, **argument.kwargs)

    def parse_argument(self, args: argparse.Namespace, ns_dest: str, argument: Argument, obj: Any) -> Any:
        """
        Parse a command-line argument value from argparse namespace and return it as a vector.Vector object.

        Args:
            args (argparse.Namespace): The argparse namespace containing the parsed command-line arguments.
            ns_dest (str): The namespace attribute name of the argument.
            argument (Argument): The Argument annotation associated with the argument.
            obj (Any): The original vector.Vector object for which the argument is defined.

        Returns:
            Any: The parsed vector.Vector object.
        """
        components = _vector.get_vector_attributes(obj)
        values = getattr(args, ns_dest)

        params = {c: values[i] for i, c in enumerate(components)}
        return vector.obj(**params)
