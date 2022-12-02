from duit.ui.PropertyRegistry import UI_PROPERTY_REGISTRY
from duit.ui.annotations import NumberAnnotation
from duit.ui.annotations.BooleanAnnotation import BooleanAnnotation
from duit.ui.tk.properties.BooleanProperty import BooleanProperty
from duit.ui.tk.properties.NumberProperty import NumberProperty


def init_tk_registry():
    UI_PROPERTY_REGISTRY[NumberAnnotation] = NumberProperty
    UI_PROPERTY_REGISTRY[BooleanAnnotation] = BooleanProperty
