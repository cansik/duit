import argparse
from typing import Type, Any

from duit.arguments.Argument import Argument
from duit.arguments.adapters.BaseTypeAdapter import BaseTypeAdapter


class DefaultTypeAdapter(BaseTypeAdapter):
    def handles_type(self, obj: Any) -> bool:
        return True

    def add_argument(self, parser, argument: Argument, obj: Any):
        parser.add_argument(argument.dest, *argument.args, **argument.kwargs)

    def parse_argument(self, args: argparse.Namespace, ns_dest: str, argument: Argument, obj: Any) -> Any:
        return getattr(args, ns_dest)
