import json
import logging
import typing
from collections.abc import Hashable
from functools import partial
from typing import Generic, TypeVar, Optional, Any, Dict, Set, Tuple, List

import numpy as np
import vector

from duit.annotation.AnnotationFinder import AnnotationFinder
from duit.model.DataField import DataField
from duit.settings.Setting import Setting
from duit.settings.serialiser.BaseSerializer import BaseSerializer
from duit.settings.serialiser.DefaultSerializer import DefaultSerializer
from duit.settings.serialiser.EnumSerializer import EnumSerializer
from duit.settings.serialiser.NumpySerializer import NumpySerializer
from duit.settings.serialiser.PathSerializer import PathSerializer
from duit.settings.serialiser.VectorSerializer import VectorSerializer
from duit.utils.name_reference import create_name_reference

T = TypeVar('T')


class Settings(Generic[T]):
    """
    A utility class for managing and serializing settings.

    Args:
        None
    """

    def __init__(self):
        """
        Initialize a Settings instance.

        Args:
            None
        """
        self.serializers: List[BaseSerializer] = [
            EnumSerializer(),
            VectorSerializer(),
            PathSerializer(),
            NumpySerializer()
        ]
        self.default_serializer: BaseSerializer = DefaultSerializer()

        self.non_unpackable_types = [vector.Vector, np.ndarray]

        self._is_serializing: bool = False
        self._is_deserializing: bool = False

        # setup annotation finder
        def _is_field_valid(field: DataField, annotation: Setting):
            if callable(field.value):
                return False

            if not annotation.exposed:
                return False
            return True

        self._annotation_finder = AnnotationFinder(Setting, _is_field_valid, recursive=False)
        self._ann_ref = create_name_reference(Setting())

    def load(self, file_path: str, obj: T) -> T:
        """
        Load settings from a file and apply them to an object.

        Args:
            file_path (str): The path to the settings file.
            obj (T): The object to which the settings will be applied.

        Returns:
            T: The object with applied settings.
        """
        with open(file_path, "r") as file:
            return self.load_json(file.read(), obj)

    def load_json(self, content: str, obj: T) -> T:
        """
        Load settings from a JSON string and apply them to an object.

        Args:
            content (str): The JSON string containing the settings.
            obj (T): The object to which the settings will be applied.

        Returns:
            T: The object with applied settings.
        """
        data = json.loads(content)
        self._deserialize(obj, data)
        return obj

    def deserialize(self, data: Dict[str, Any], obj: T) -> T:
        """
        Deserialize a dictionary of settings and apply them to an object.

        Args:
            data (Dict[str, Any]): The dictionary containing the settings.
            obj (T): The object to which the settings will be applied.

        Returns:
            T: The object with applied settings.
        """
        self._is_deserializing = True
        result = self._deserialize(obj, data)
        self._is_deserializing = False
        return result

    def save(self, file_path: str, obj: T):
        """
        Save settings from an object to a file.

        Args:
            file_path (str): The path to the settings file.
            obj (T): The object from which settings will be saved.

        Returns:
            None
        """
        data = self.save_json(obj)
        with open(file_path, "w") as file:
            file.write(data)

    def save_json(self, obj: T) -> str:
        """
        Save settings from an object to a JSON string.

        Args:
            obj (T): The object from which settings will be saved.

        Returns:
            str: The JSON string containing the settings.
        """
        data = self._serialize(obj)
        return json.dumps(data, indent=4, sort_keys=True)

    def serialize(self, obj: T) -> Dict[str, Any]:
        """
        Serialize settings from an object to a dictionary.

        Args:
            obj (T): The object from which settings will be serialized.

        Returns:
            Dict[str, Any]: The dictionary containing the settings.
        """
        self._is_serializing = True
        result = self._serialize(obj)
        self._is_serializing = False
        return result

    def _serialize(self, obj: Any,
                   data: Optional[Dict[str, Any]] = None,
                   obj_history: Optional[Set[Any]] = None) -> Dict[str, Any]:
        if obj_history is None:
            obj_history = set()

        if isinstance(obj, Hashable) and obj in obj_history:
            return {}

        if data is None:
            data = {}

        if isinstance(obj, Hashable):
            obj_history.add(obj)

        # extract data-model fields
        fields = self._annotation_finder.find(obj)
        field_list = sorted(fields.items(), key=partial(self._annotation_sorting, self._ann_ref.save_order))
        field_list = typing.cast(List[Tuple[str, Tuple[DataField, Setting]]], field_list)

        # fill datamodel fields into data
        for name, values in field_list:
            field, setting = values

            if setting.name is not None:
                name = setting.name

            # check which serializer to use
            serializer = self._get_matching_serializer(field)
            success, value = serializer.serialize(field.value)

            if success:
                data[name] = value
            else:
                logging.warning(f"Could not serialize '{name}': {field.value}")

            # call again for each datamodel value to catch subfields
            result = self._serialize(field.value, {}, obj_history)
            if len(result) != 0:
                data[name] = result

            if not self._is_jsonable(data[name]):
                logging.warning(f"Could not convert '{name}' to json: {field.value}")
                data.pop(name)
                continue

        return data

    def _deserialize(self, obj: Any, data: Dict[str, Any],
                     obj_history: Optional[Set[Any]] = None) -> Tuple[bool, Any]:
        if obj_history is None:
            obj_history = set()

        if isinstance(obj, Hashable) and obj in obj_history:
            return True, obj

        if not isinstance(data, Dict):
            return False, None

        for t in self.non_unpackable_types:
            if isinstance(obj, t):
                return False, None

        if isinstance(obj, Hashable):
            obj_history.add(obj)

        # create string to field index
        fields_table: Dict[str, Any] = {}

        fields = self._annotation_finder.find(obj)
        field_list = sorted(fields.items(), key=partial(self._annotation_sorting, self._ann_ref.load_order))
        field_list = typing.cast(List[Tuple[str, Tuple[DataField, Setting]]], field_list)

        # create name to field table
        for name, values in field_list:
            field, setting = values

            if setting.name is not None:
                name = setting.name
            fields_table.update({name: field})

        # map data to fields
        for name, values in field_list:
            field, setting = values
            key = name if setting.name is None else setting.name
            if key not in data:
                continue
            raw_value = data[key]

            # check if is subtype
            success, sub_obj = self._deserialize(field.value, raw_value, obj_history)
            if success and type(field.value) == type(sub_obj):
                field.value = sub_obj
                continue

            serializer = self._get_matching_serializer(field)
            success, value = serializer.deserialize(type(field.value), raw_value)

            if success:
                field.value = value
            else:
                logging.warning(f"Could not deserialize {key}: {raw_value}")

        return True, obj

    def _get_matching_serializer(self, field: DataField) -> BaseSerializer:
        for serializer in self.serializers:
            if serializer.handles_type(field.value):
                return serializer
        return self.default_serializer

    @staticmethod
    def _annotation_sorting(sort_key: str, item: Tuple[str, Tuple[DataField, Setting]]) -> int:
        _, values = item
        _, ann = values
        return getattr(ann, sort_key)

    @staticmethod
    def _is_jsonable(x):
        try:
            json.dumps(x)
            return True
        except (TypeError, OverflowError):
            return False

    @property
    def is_serializing(self) -> bool:
        return self._is_serializing

    @property
    def is_deserializing(self) -> bool:
        return self.is_deserializing


DefaultSettings = Settings()
