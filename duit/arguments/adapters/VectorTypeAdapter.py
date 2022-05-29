import argparse
from typing import Any

import vector

from duit.arguments.Argument import Argument
from duit.arguments.adapters.BaseTypeAdapter import BaseTypeAdapter
from duit.utils import _vector


class VectorTypeAdapter(BaseTypeAdapter):
    def handles_type(self, obj: Any) -> bool:
        return isinstance(obj, vector.Vector)

    def add_argument(self, parser, argument: Argument, obj: Any):
        components = _vector.get_vector_attributes(obj)

        argument.kwargs["metavar"] = components
        argument.kwargs["type"] = float
        argument.kwargs["nargs"] = len(components)
        argument.kwargs["default"] = [getattr(obj, c) for c in components]

        parser.add_argument(argument.dest, *argument.args, **argument.kwargs)

    def parse_argument(self, args: argparse.Namespace, ns_dest: str, argument: Argument, obj: Any) -> Any:
        components = _vector.get_vector_attributes(obj)
        values = getattr(args, ns_dest)

        params = {c: values[i] for i, c in enumerate(components)}
        return vector.obj(**params)
