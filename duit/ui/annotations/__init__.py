from typing import Dict, Tuple, List

from duit.model.DataField import DataField
from duit.ui.annotations.UIAnnotation import UIAnnotation, UI_ANNOTATION_ATTRIBUTE_NAME
from duit.ui.annotations.NumberAnnotation import NumberAnnotation


def find_all_ui_annotations(ctx) -> Dict[str, Tuple[DataField, List[UIAnnotation]]]:
    annotations = {}
    for n, v in ctx.__dict__.items():
        if isinstance(v, DataField) and hasattr(v, UI_ANNOTATION_ATTRIBUTE_NAME):
            annotations[n] = (v, v.__getattribute__(UI_ANNOTATION_ATTRIBUTE_NAME))
    return annotations
