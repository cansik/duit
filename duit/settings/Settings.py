from collections.abc import Hashable
import json
import logging
from typing import Generic, TypeVar, Optional, Any, Dict, Set, Tuple, List

import vector

from duit.annotation.AnnotationFinder import AnnotationFinder
from duit.model.DataField import DataField
from duit.settings import SETTING_ANNOTATION_ATTRIBUTE_NAME
from duit.settings.Setting import Setting
from duit.settings.serialiser.BaseSerializer import BaseSerializer
from duit.settings.serialiser.DefaultSerializer import DefaultSerializer
from duit.settings.serialiser.EnumSerializer import EnumSerializer
from duit.settings.serialiser.PathSerializer import PathSerializer
from duit.settings.serialiser.VectorSerializer import VectorSerializer

T = TypeVar('T')


class Settings(Generic[T]):
    def __init__(self):
        self.serializers: List[BaseSerializer] = [
            EnumSerializer(),
            VectorSerializer(),
            PathSerializer()
        ]
        self.default_serializer: BaseSerializer = DefaultSerializer()

        self.non_unpackable_type = [vector.Vector]

        # setup annotation finder
        def _is_field_valid(field: DataField, annotation: Setting):
            if callable(field.value):
                return False

            if not annotation.exposed:
                return False
            return True

        self._annotation_finder = AnnotationFinder(Setting, _is_field_valid, recursive=False)

    def load(self, file_path: str, obj: T) -> T:
        with open(file_path, "r") as file:
            return self.load_json(file.read(), obj)

    def load_json(self, content: str, obj: T) -> T:
        data = json.loads(content)
        self._deserialize(obj, data)
        return obj

    def save(self, file_path: str, obj: T):
        data = self.save_json(obj)
        with open(file_path, "w") as file:
            file.write(data)

    def save_json(self, obj: T) -> str:
        data = self._serialize(obj)
        return json.dumps(data, indent=4, sort_keys=True)

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

        # extract datamodel fields
        fields = self._annotation_finder.find(obj)

        # fill datamodel fields into data
        for name, values in fields.items():
            field, setting = values

            if setting.name is not None:
                name = setting.name

            # check which serializer to use
            serializer = self._get_matching_serializer(field)
            success, value = serializer.serialize(field.value)

            if success:
                data[name] = value
            else:
                logging.warning(f"Could not serialize {name}: {field.value}")

            # call again for each datamodel value to catch subfields
            result = self._serialize(field.value, {}, obj_history)
            if len(result) != 0:
                data[name] = result

            if not self._is_jsonable(data[name]):
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

        for t in self.non_unpackable_type:
            if isinstance(obj, t):
                return False, None

        if isinstance(obj, Hashable):
            obj_history.add(obj)

        # create string to field index
        fields_table: Dict[str, Any] = {}
        fields = self._annotation_finder.find(obj)
        for name, values in fields.items():
            field, setting = values

            if setting.name is not None:
                name = setting.name
            fields_table.update({name: field})

        # map data to fields
        for key, raw_value in data.items():
            if key not in fields_table:
                continue
            field: DataField = fields_table[key]

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
    def _is_jsonable(x):
        try:
            json.dumps(x)
            return True
        except (TypeError, OverflowError):
            return False
