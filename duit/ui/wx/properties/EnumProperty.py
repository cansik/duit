from typing import Any, List

from duit.ui.wx.properties.OptionsProperty import OptionsProperty


class EnumProperty(OptionsProperty):
    """
    Property class for handling enum-based fields in a Wx-based UI.

    This property displays an enum field in a Wx UI, allowing the user to select from a list of predefined options.

    Attributes:
        options (List[Any]): The list of available enum options.
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
