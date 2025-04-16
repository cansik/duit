from dataclasses import dataclass, field
from typing import List, Any


@dataclass(frozen=True)
class AttributeIdentifier:
    name: str
    parents: List[str] = field(default_factory=list)

    def get_value(self, obj: Any) -> Any:
        pass

    def set_value(self, obj: Any) -> Any:
        pass

    def __str__(self):
        return f"{self.__name__} ({self.path})"

    def __repr__(self):
        self.__str__()

    @property
    def path(self) -> str:
        return self.get_path_separator().join([*self.parents, self.name])

    @staticmethod
    def get_path_separator() -> str:
        return "."

    @staticmethod
    def from_path(path: str) -> "AttributeIdentifier":
        elements = path.split(AttributeIdentifier.get_path_separator())
        return AttributeIdentifier(elements.pop(), elements)

    def __hash__(self):
        return hash(self.path)
