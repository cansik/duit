import json
from typing import Generic, TypeVar, Optional, Any, Dict, Set, Tuple

from simbi.model.DataField import DataField
from simbi.settings import SETTING_ANNOTATION_ATTRIBUTE_NAME
from simbi.settings.Setting import Setting

T = TypeVar('T')


class Settings(Generic[T]):
    def __init__(self):
        pass

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
        if data is None:
            data = {}

        if obj_history is None:
            obj_history = set()

        obj_history.add(obj)

        # extract datamodel fields
        fields = self._find_all_setting_annotations(obj)

        # fill datamodel fields into data
        for name, values in fields.items():
            field, setting = values

            if setting.name is not None:
                name = setting.name

            # todo: implement specific deserializer
            data[name] = field.value

            # call again for each datamodel value to catch subfields
            # self._serialize(field.value, {}, obj_history)

        return data

    @staticmethod
    def _find_all_setting_annotations(obj: Any, filter_exposed: bool = True) -> Dict[str, Tuple[DataField, Setting]]:
        annotations = {}
        for n, v in obj.__dict__.items():
            if isinstance(v, DataField) and hasattr(v, SETTING_ANNOTATION_ATTRIBUTE_NAME):
                setting: Setting = v.__getattribute__(SETTING_ANNOTATION_ATTRIBUTE_NAME)
                if filter_exposed and not setting.exposed:
                    continue

                if callable(v.value):
                    continue

                annotations[n] = (v, v.__getattribute__(SETTING_ANNOTATION_ATTRIBUTE_NAME))
        return annotations
