from typing import Any, List

from duit.ui.open3d.properties.OptionsProperty import OptionsProperty


class EnumProperty(OptionsProperty):
    """
    Property class for handling EnumAnnotation.

    This property generates a dropdown widget for selecting enum values.

    """

    @property
    def options(self) -> List[Any]:
        """
        Get the list of available enum options.

        :return: A list of available enum options.
        """
        enum_type = type(self.model.value)
        return list(enum_type)

    def get_option_name(self, option) -> str:
        """
        Get the name of an enum option.

        :param option: The enum option for which to retrieve the name.
        :return: The name of the enum option.
        """
        return option.name
