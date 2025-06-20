from typing import Any, List

from duit.ui.nicegui.properties.OptionsProperty import OptionsProperty


class EnumProperty(OptionsProperty):
    """
    A property class that represents an enumeration, providing options based on the available enum members.
    """

    @property
    def options(self) -> List[Any]:
        """
        Get the list of available enum options.

        Returns:
            List[Any]: A list of available enum options.
        """
        enum_type = type(self.model.value)
        return list(enum_type)

    def get_option_name(self, option) -> str:
        """
        Get the name of the provided enum option.

        Args:
            option (Any): The enum option.

        Returns:
            str: The name of the enum option.
        """
        return option.name
