import argparse
from typing import Type, Any

from duit.arguments.Argument import Argument
from duit.arguments.adapters.BaseTypeAdapter import BaseTypeAdapter


class EnumTypeAdapter(BaseTypeAdapter):
    def handles_type(self, obj: Any) -> bool:
        return False

    def add_argument(self, parser, argument: Argument, data_type: Type) -> Argument:
        pass

    def parse_argument(self, args: argparse.Namespace, dest: str, argument: Argument, data_type: Type) -> Any:
        pass
