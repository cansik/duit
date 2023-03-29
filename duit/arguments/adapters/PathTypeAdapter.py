import argparse
from pathlib import Path
from typing import Type, Any

from duit.arguments.Argument import Argument
from duit.arguments.adapters.BaseTypeAdapter import BaseTypeAdapter


class PathTypeAdapter(BaseTypeAdapter):
    def handles_type(self, obj: Any) -> bool:
        return isinstance(obj, Path)

    def add_argument(self, parser, argument: Argument, obj: Any):
        parser.add_argument(argument.dest, *argument.args, **argument.kwargs)

    def parse_argument(self, args: argparse.Namespace, ns_dest: str, argument: Argument, obj: Any) -> Path:
        return Path(getattr(args, ns_dest))
