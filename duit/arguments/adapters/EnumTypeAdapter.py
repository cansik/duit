import argparse
from enum import Enum
from typing import Type, Any

from duit.arguments.Argument import Argument
from duit.arguments.adapters.BaseTypeAdapter import BaseTypeAdapter


class EnumTypeAdapter(BaseTypeAdapter):
    def handles_type(self, obj: Any) -> bool:
        return isinstance(obj, Enum)

    def add_argument(self, parser, argument: Argument, obj: Enum):
        items = {item.name: item for item in list(type(obj))}

        argument.kwargs["default"] = obj.name
        argument.kwargs["metavar"] = ", ".join([v for v in items.keys()])
        argument.kwargs["type"] = str

        parser.add_argument(argument.dest, *argument.args, **argument.kwargs)

    def parse_argument(self, args: argparse.Namespace, ns_dest: str, argument: Argument, obj: Any) -> Any:
        items = {item.name: item for item in list(type(obj))}
        raw_value = getattr(args, ns_dest)

        return items[raw_value]
