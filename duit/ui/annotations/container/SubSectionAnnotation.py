from typing import Optional

from duit.model.DataField import DataField
from duit.ui.annotations.container.StartSectionAnnotation import StartSectionAnnotation


class SubSectionAnnotation(StartSectionAnnotation):
    def __init__(self, name: str, collapsed: bool = False, is_active_field: Optional[DataField[bool]] = None):
        super().__init__(name, collapsed, is_active_field)
