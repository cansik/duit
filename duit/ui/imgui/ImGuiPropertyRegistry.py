from duit.ui.PropertyRegistry import UI_PROPERTY_REGISTRY
from duit.ui.annotations.BooleanAnnotation import BooleanAnnotation


def init_imgui_registry():
    UI_PROPERTY_REGISTRY[BooleanAnnotation] = None