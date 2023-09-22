import argparse
from collections import defaultdict
from typing import Any, List

from duit.annotation.AnnotationFinder import AnnotationFinder
from duit.arguments.Argument import Argument
from duit.arguments.adapters.BaseTypeAdapter import BaseTypeAdapter
from duit.arguments.adapters.DefaultTypeAdapter import DefaultTypeAdapter
from duit.arguments.adapters.EnumTypeAdapter import EnumTypeAdapter
from duit.arguments.adapters.PathTypeAdapter import PathTypeAdapter
from duit.arguments.adapters.VectorTypeAdapter import VectorTypeAdapter
from duit.model.DataField import DataField


class Arguments:
    def __init__(self):
        self.type_adapters: List[BaseTypeAdapter] = [
            EnumTypeAdapter(),
            VectorTypeAdapter(),
            PathTypeAdapter()
        ]
        self.default_serializer: BaseTypeAdapter = DefaultTypeAdapter()

        # setup annotation finder
        def _is_field_valid(field: DataField, annotation: Argument):
            if callable(field.value):
                return False
            return True

        self._annotation_finder = AnnotationFinder(Argument, _is_field_valid, recursive=True)

    def add_and_configure(self, parser: argparse.ArgumentParser, obj: Any) -> argparse.Namespace:
        self.add_arguments(parser, obj)
        args = parser.parse_args()
        self.configure(args, obj)
        return args

    def add_arguments(self, parser: argparse.ArgumentParser, obj: Any):
        groups = defaultdict(list)

        for name, (field, argument) in self._annotation_finder.find(obj).items():
            if argument.dest is None:
                argument.dest = f"--{self._to_argument_str(name)}"

            groups[argument.group].append((field, argument))

        group_keys = sorted(groups.keys())
        if None in group_keys:
            group_keys.remove(None)
            group_keys.insert(0, None)

        parser_groups = {g: parser.add_argument_group(g) for g in group_keys if g is not None}
        parser_groups[None] = parser

        for key in group_keys:
            p = parser_groups[key]

            for field, argument in groups[key]:
                type_adapter = self._get_matching_type_adapter(field)
                type_adapter.add_argument(p, argument, field.value)

    def configure(self, args: argparse.Namespace, obj: Any):
        for name, (field, argument) in self._annotation_finder.find(obj).items():
            dest = name if argument.dest is None else argument.dest
            ns_dest = self._to_namespace_str(dest)
            type_adapter = self._get_matching_type_adapter(field)
            field.value = type_adapter.parse_argument(args, ns_dest, argument, field.value)

    def update_namespace(self, namespace: argparse.Namespace, obj: Any):
        for name, (field, argument) in self._annotation_finder.find(obj).items():
            dest = name if argument.dest is None else argument.dest
            ns_dest = self._to_namespace_str(dest)
            namespace.__setattr__(ns_dest, field.value)

    def _get_matching_type_adapter(self, field: DataField) -> BaseTypeAdapter:
        for type_adapter in self.type_adapters:
            if type_adapter.handles_type(field.value):
                return type_adapter
        return self.default_serializer

    @staticmethod
    def _to_argument_str(name: str) -> str:
        return name.replace("_", "-")

    @staticmethod
    def _to_namespace_str(name: str) -> str:
        if name.startswith("--"):
            name = name[2:]

        return name.replace("-", "_")
