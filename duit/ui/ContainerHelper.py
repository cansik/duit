import re
from typing import Any

from duit.collections.Stack import Stack
from duit.model.DataField import DataField
from duit.settings.Setting import Setting
from duit.ui.annotations.container.EndSectionAnnotation import EndSectionAnnotation
from duit.ui.annotations.container.StartSectionAnnotation import StartSectionAnnotation


class ContainerHelper:

    def __init__(self, obj: Any):
        self._obj = obj
        self._section_stack: Stack[str] = Stack()

    @staticmethod
    def _create_field_name(name: str) -> str:
        regex = r"([\W])"
        result = re.sub(regex, "_", name, 0, re.MULTILINE)
        return result.lower()

    def start_section(self, name: str, collapsed: bool = False):
        field = DataField(None) | StartSectionAnnotation(name, collapsed) | Setting(exposed=False)
        attribute_name = self._create_field_name(name)
        self._section_stack.push(attribute_name)
        setattr(self._obj, f"__duit_start_section_{attribute_name}", field)

    def end_section(self):
        field = DataField(None) | EndSectionAnnotation() | Setting(exposed=False)
        attribute_name = self._section_stack.pop()
        setattr(self._obj, f"__duit_end_section_{attribute_name}", field)

    def section(self, name: str, collapsed: bool = False) -> "ContainerHelper":
        self.start_section(name, collapsed)
        return self

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_section()

