from typing import Generic, TypeVar

T = TypeVar("T")


class NameReferenceDecorator(Generic[T]):
    def __init__(self, obj: T):
        self.obj = obj

    def __getattribute__(self, item) -> str:
        return item


def create_name_reference(obj: T) -> T:
    decorator = NameReferenceDecorator(obj)
    return decorator
