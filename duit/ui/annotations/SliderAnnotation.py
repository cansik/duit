from typing import Optional

from duit.ui.annotations import NumberAnnotation


class SliderAnnotation(NumberAnnotation):
    def __init__(self, name: str, limit_min: float = 0, limit_max: float = 1, step_size: Optional[float] = None,
                 tooltip: str = "", readonly: bool = False, show_number_field: bool = True):
        """
        Initialize a SliderAnnotation.

        :param name: The name of the slider annotation.
        :param limit_min: The minimum allowable value for the slider.
        :param limit_max: The maximum allowable value for the slider.
        :param step_size: The step size for the slider.
        :param tooltip: The tooltip text for the annotation.
        :param readonly: Whether the annotation is read-only (default is False).
        :param show_number_field: Whether to display a number field next to the slider (default is True).
        """
        super().__init__(name, limit_min, limit_max, 3, tooltip, readonly)
        self.show_number_field = show_number_field
        self.step_size = step_size
