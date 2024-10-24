import re
from typing import Any, Optional

from duit.collections.Stack import Stack
from duit.model.DataField import DataField
from duit.settings.Setting import Setting
from duit.ui.annotations.container.EndSectionAnnotation import EndSectionAnnotation
from duit.ui.annotations.container.StartSectionAnnotation import StartSectionAnnotation


class ContainerHelper:
    def __init__(self, obj: Any):
        """
        Initialize a ContainerHelper.

        :param obj: The object to which sections are added.
        """
        self._obj = obj
        self._section_stack: Stack[str] = Stack()

    @staticmethod
    def _create_field_name(name: str) -> str:
        """
        Create a field name from a section name.

        This method converts a section name into a valid field name by replacing
        non-word characters with underscores and converting the result to lowercase.

        :param name: The section name.
        :return: A valid field name.
        """
        regex = r"([\W])"
        result = re.sub(regex, "_", name, 0, re.MULTILINE)
        return result.lower()

    def start_section(self, name: str, collapsed: bool = False, is_active_field: Optional[DataField[bool]] = None):
        """
        Start a new section.

        :param name: The name of the section.
        :param collapsed: Whether the section should be initially collapsed.
        :param is_active_field: An optional DataField that determines the active state of the section.
        """
        field = DataField(None) | StartSectionAnnotation(name, collapsed, is_active_field) | Setting(exposed=False)
        attribute_name = self._create_field_name(name)
        self._section_stack.push(attribute_name)
        setattr(self._obj, f"__duit_start_section_{attribute_name}", field)

    def end_section(self):
        """
        End the current section.
        """
        field = DataField(None) | EndSectionAnnotation() | Setting(exposed=False)
        attribute_name = self._section_stack.pop()
        setattr(self._obj, f"__duit_end_section_{attribute_name}", field)

    def section(self, name: str, collapsed: bool = False,
                is_active_field: Optional[DataField[bool]] = None) -> "ContainerHelper":
        """
        Start a new section and return the ContainerHelper for chaining.

        :param name: The name of the section.
        :param collapsed: Whether the section should be initially collapsed.
        :param is_active_field: An optional DataField that determines the active state of the section.
        :return: The ContainerHelper for chaining.
        """
        self.start_section(name, collapsed, is_active_field)
        return self

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_section()
