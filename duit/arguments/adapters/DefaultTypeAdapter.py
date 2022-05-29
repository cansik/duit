import argparse
from typing import Type, Any

from duit.arguments.Argument import Argument
from duit.arguments.adapters.BaseTypeAdapter import BaseTypeAdapter


class DefaultTypeAdapter(BaseTypeAdapter):
    def handles_type(self, obj: Any) -> bool:
        return True

    def add_argument(self, parser, argument: Argument, data_type: Type):
        parser.add_argument(argument.dest, *argument.args, **argument.kwargs)

    def parse_argument(self, args: argparse.Namespace, dest: str, argument: Argument, data_type: Type) -> Any:
        return getattr(args, dest)
