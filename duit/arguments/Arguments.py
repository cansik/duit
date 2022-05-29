import argparse
from collections import defaultdict
from typing import Any, Dict, Tuple

from duit.arguments import ARGUMENT_ANNOTATION_ATTRIBUTE_NAME
from duit.arguments.Argument import Argument
from duit.model.DataField import DataField


class Arguments:
    def add_and_configure(self, parser: argparse.ArgumentParser, obj: Any) -> argparse.Namespace:
        self.add_arguments(parser, obj)
        args = parser.parse_args()
        self.configure(args, obj)
        return args

    def add_arguments(self, parser: argparse.ArgumentParser, obj: Any):
        groups = defaultdict(list)

        for name, (field, argument) in self._find_all_argument_annotations(obj).items():
            if argument.dest is None:
                argument.dest = f"--{self._to_argument_str(name)}"

            groups[argument.group].append(argument)

        group_keys = sorted(groups.keys())
        if None in group_keys:
            group_keys.remove(None)
            group_keys.insert(0, None)

        parser_groups = {g: parser.add_argument_group(g) for g in group_keys if g is not None}
        parser_groups[None] = parser

        for key in group_keys:
            p = parser_groups[key]

            for argument in groups[key]:
                p.add_argument(argument.dest, *argument.args, **argument.kwargs)

    def configure(self, args: argparse.Namespace, obj: Any):
        for name, (field, argument) in self._find_all_argument_annotations(obj).items():
            dest = self._to_namespace_str(argument.dest)

            if dest in args:
                field.value = getattr(args, dest)

    @staticmethod
    def _find_all_argument_annotations(obj: Any) -> Dict[str, Tuple[DataField, Argument]]:
        annotations = {}

        if not hasattr(obj, "__dict__"):
            return annotations

        for n, v in obj.__dict__.items():
            if isinstance(v, DataField):
                if hasattr(v, ARGUMENT_ANNOTATION_ATTRIBUTE_NAME):
                    if callable(v.value):
                        continue
                    annotations[n] = (v, v.__getattribute__(ARGUMENT_ANNOTATION_ATTRIBUTE_NAME))
                else:
                    annotations.update(Arguments._find_all_argument_annotations(v.value))
        return annotations

    @staticmethod
    def _to_argument_str(name: str) -> str:
        return name.replace("_", "-")

    @staticmethod
    def _to_namespace_str(name: str) -> str:
        if name.startswith("--"):
            name = name[2:]

        return name.replace("-", "_")
