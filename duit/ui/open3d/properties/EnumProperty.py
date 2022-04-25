from typing import Any, List

from duit.ui.open3d.properties.OptionsProperty import OptionsProperty


class EnumProperty(OptionsProperty):
    @property
    def options(self) -> List[Any]:
        enum_type = type(self.model.value)
        return list(enum_type)

    def get_option_name(self, option) -> str:
        return option.name
