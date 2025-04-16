import argparse
from collections import defaultdict
from typing import Any, List

from duit.annotation.AnnotationFinder import AnnotationFinder
from duit.arguments.Argument import Argument
from duit.arguments.adapters.BaseTypeAdapter import BaseTypeAdapter
from duit.arguments.adapters.BooleanTypeAdapter import BooleanTypeAdapter
from duit.arguments.adapters.DefaultTypeAdapter import DefaultTypeAdapter
from duit.arguments.adapters.EnumTypeAdapter import EnumTypeAdapter
from duit.arguments.adapters.PathTypeAdapter import PathTypeAdapter
from duit.arguments.adapters.VectorTypeAdapter import VectorTypeAdapter
from duit.model.DataField import DataField


class Arguments:
    """
    A class for handling command-line arguments based on annotations in objects.

    Attributes:
        type_adapters (List[BaseTypeAdapter]): A list of type adapters to handle specific data types.
        default_serializer (BaseTypeAdapter): The default type adapter for serialization.
        _annotation_finder (AnnotationFinder): An instance of AnnotationFinder for finding Argument annotations in objects.
    """

    def __init__(self):
        """
        Initialize an Arguments instance with default configuration.
        """
        self.type_adapters: List[BaseTypeAdapter] = [
            BooleanTypeAdapter(),
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

        self._annotation_finder: AnnotationFinder[Argument] = AnnotationFinder(Argument, _is_field_valid,
                                                                               recursive=True)

    def add_and_configure(self,
                          parser: argparse.ArgumentParser,
                          obj: Any,
                          use_attribute_path_as_name: bool = False) -> argparse.Namespace:
        """
        Add command-line arguments to the parser and configure them based on annotations in the object.

        Args:
            parser (argparse.ArgumentParser): The argparse parser to which the arguments will be added.
            obj (Any): The object containing annotations for command-line arguments.
            use_attribute_path_as_name (bool): Use the attribute path as name. This allows nested attributes share the same name.

        Returns:
            argparse.Namespace: The parsed namespace containing the configured command-line arguments.
        """
        self.add_arguments(parser, obj, use_attribute_path_as_name)
        args = parser.parse_args()
        self.configure(args, obj)
        return args

    def add_arguments(self,
                      parser: argparse.ArgumentParser, obj: Any,
                      use_attribute_path_as_name: bool = False):
        """
        Add command-line arguments to the parser based on annotations in the object.

        Args:
            parser (argparse.ArgumentParser): The argparse parser to which the arguments will be added.
            obj (Any): The object containing annotations for command-line arguments.
            use_attribute_path_as_name (bool): Use the attribute path as name. This allows nested attributes share the same name.
        """
        groups = defaultdict(list)

        for attribute_identifier, (field, argument) in self._annotation_finder.find_with_identifier(obj).items():
            if argument.dest is None:
                attribute_name = attribute_identifier.path if use_attribute_path_as_name else attribute_identifier.name
                argument.dest = f"--{self.to_argument_str(attribute_name)}"

            groups[argument.group].append((field, argument))

        group_keys = sorted(groups.keys(), key=lambda x: (x is not None, x))
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
        """
        Configure object fields based on the parsed command-line arguments.

        Args:
            args (argparse.Namespace): The parsed namespace containing the command-line arguments.
            obj (Any): The object containing annotations for command-line arguments.
        """
        for name, (field, argument) in self._annotation_finder.find(obj).items():
            dest = name if argument.dest is None else argument.dest
            ns_dest = self.to_namespace_str(dest)

            if not argument.allow_none and getattr(args, ns_dest) is None:
                continue

            type_adapter = self._get_matching_type_adapter(field)
            field.value = type_adapter.parse_argument(args, ns_dest, argument, field.value)

    def update_namespace(self, namespace: argparse.Namespace, obj: Any):
        """
        Update the argparse namespace with the object's field values.

        Args:
            namespace (argparse.Namespace): The argparse namespace to be updated.
            obj (Any): The object containing annotations for command-line arguments.
        """
        for name, (field, argument) in self._annotation_finder.find(obj).items():
            dest = name if argument.dest is None else argument.dest
            ns_dest = self.to_namespace_str(dest)
            namespace.__setattr__(ns_dest, field.value)

    def _get_matching_type_adapter(self, field: DataField) -> BaseTypeAdapter:
        """
        Get the type adapter that matches the data type of a field.

        Args:
            field (DataField): The DataField with a specific data type.

        Returns:
            BaseTypeAdapter: The type adapter that matches the data type, or the default serializer if no match is found.
        """
        for type_adapter in self.type_adapters:
            if type_adapter.handles_type(field.value):
                return type_adapter
        return self.default_serializer

    @staticmethod
    def to_argument_str(name: str) -> str:
        """
        Convert a name to a format suitable for command-line arguments (replace underscores with dashes).

        Args:
            name (str): The original name.

        Returns:
            str: The name in the format suitable for command-line arguments.
        """
        return name.replace("_", "-")

    @staticmethod
    def to_namespace_str(name: str) -> str:
        """
        Convert a command-line argument name to a namespace attribute name (replace dashes with underscores).

        Args:
            name (str): The command-line argument name.

        Returns:
            str: The corresponding namespace attribute name.
        """

        if name.startswith("--"):
            name = name[2:]

        return name.replace("-", "_")


DefaultArguments = Arguments()
