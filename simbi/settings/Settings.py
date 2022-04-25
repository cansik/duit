import json
import logging
from typing import Generic, TypeVar, Optional, Any, Dict, Set, Tuple, List

from simbi.model.DataField import DataField
from simbi.settings import SETTING_ANNOTATION_ATTRIBUTE_NAME
from simbi.settings.Setting import Setting
from simbi.settings.serialiser.BaseSerializer import BaseSerializer
from simbi.settings.serialiser.DefaultSerializer import DefaultSerializer

T = TypeVar('T')


class Settings(Generic[T]):
    def __init__(self):
        self.serializers: List[BaseSerializer] = []
        self.default_serializer: BaseSerializer = DefaultSerializer()

    def load(self, file_path: str, obj: Optional[T] = None) -> T:
        with open(file_path, "r") as file:
            return self.load_json(file.read(), obj)

    def load_json(self, content: str, obj: Optional[T] = None) -> T:
        pass

    def save(self, file_path: str, obj: T):
        with open(file_path, "w") as file:
            file.write(self.save_json(obj))

    def save_json(self, obj: T) -> str:
        data = self._serialize(obj)
        return json.dumps(data, indent=4, sort_keys=True)

    def _serialize(self, obj: Any,
                   data: Optional[Dict[str, Any]] = None,
                   obj_history: Optional[Set[Any]] = None) -> Dict[str, Any]:
        if obj_history is None:
            obj_history = set()

        if obj in obj_history:
            return {}

        if data is None:
            data = {}

        obj_history.add(obj)

        # extract datamodel fields
        fields = self._find_all_setting_annotations(obj)

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
                logging.warning(f"Could not serialize {name}.")

            # call again for each datamodel value to catch subfields
            result = self._serialize(field.value, {}, obj_history)
            if len(result) != 0:
                data[name] = result

        return data

    def _get_matching_serializer(self, field: DataField) -> BaseSerializer:
        for serializer in self.serializers:
            if serializer.handles_type(field.value):
                return serializer
        return self.default_serializer

    @staticmethod
    def _find_all_setting_annotations(obj: Any, filter_exposed: bool = True) -> Dict[str, Tuple[DataField, Setting]]:
        annotations = {}

        if not hasattr(obj, "__dict__"):
            return annotations

        for n, v in obj.__dict__.items():
            if isinstance(v, DataField) and hasattr(v, SETTING_ANNOTATION_ATTRIBUTE_NAME):
                setting: Setting = v.__getattribute__(SETTING_ANNOTATION_ATTRIBUTE_NAME)
                if filter_exposed and not setting.exposed:
                    continue

                if callable(v.value):
                    continue

                annotations[n] = (v, v.__getattribute__(SETTING_ANNOTATION_ATTRIBUTE_NAME))
        return annotations
