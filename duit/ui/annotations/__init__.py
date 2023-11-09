from typing import Dict, Tuple, List

from duit.model.DataField import DataField
from duit.ui.annotations.NumberAnnotation import NumberAnnotation
from duit.ui.annotations.UIAnnotation import UIAnnotation, UI_ANNOTATION_ATTRIBUTE_NAME


def find_all_ui_annotations(ctx) -> Dict[str, Tuple[DataField, List[UIAnnotation]]]:
    """
    Find all UI annotations in the given context.

    This function searches for UI annotations within the attributes of the given context and
    returns a dictionary with the names of the attributes containing UI annotations and the associated
    DataField objects along with the list of UI annotations applied to them.

    :param ctx: The context in which to search for UI annotations.
    :return: A dictionary of attribute names to (DataField, List[UIAnnotation]) pairs.
    """
    annotations = {}
    for n, v in ctx.__dict__.items():
        if isinstance(v, DataField) and hasattr(v, UI_ANNOTATION_ATTRIBUTE_NAME):
            annotations[n] = (v, v.__getattribute__(UI_ANNOTATION_ATTRIBUTE_NAME))
    return annotations
