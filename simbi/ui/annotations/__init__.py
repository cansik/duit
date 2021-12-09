from typing import Dict, Tuple, List

from simbi.model.DataModel import DataModel
from simbi.ui.annotations.UIAnnotation import UIAnnotation, UI_ANNOTATION_ATTRIBUTE_NAME
from simbi.ui.annotations.NumberAnnotation import NumberAnnotation


def find_all_ui_annotations(ctx) -> Dict[str, Tuple[DataModel, List[UIAnnotation]]]:
    annotations = {}
    for n, v in ctx.__dict__.items():
        if isinstance(v, DataModel) and hasattr(v, UI_ANNOTATION_ATTRIBUTE_NAME):
            annotations[n] = (v, v.__getattribute__(UI_ANNOTATION_ATTRIBUTE_NAME))
    return annotations
