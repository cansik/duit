from typing import Generic, TypeVar, Optional

SETTING_ANNOTATION_ATTRIBUTE_NAME = "__simbi_settings_annotation"
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
        return ""
