from typing import Optional

from duit.model.DataField import DataField
from duit.ui.annotations.container.StartSectionAnnotation import StartSectionAnnotation


class SubSectionAnnotation(StartSectionAnnotation):
    def __init__(self, name: str, collapsed: bool = False,
                 is_active_field: Optional[DataField[bool]] = None,
                 name_field: Optional[DataField[str]] = None):
        """
        Initialize a SubSectionAnnotation.

        This annotation is used to mark the start of a subsection within a section of a user interface.

        :param name: The name or title of the subsection.
        :param collapsed: Whether the subsection should be initially collapsed (default is False).
        :param is_active_field: An optional DataField that determines the active state of the subsection.
        :param name_field: An optional DataField that can be used for dynamic names.
        """
        super().__init__(name, collapsed, is_active_field, name_field)
