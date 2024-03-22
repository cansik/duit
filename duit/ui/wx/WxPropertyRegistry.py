from duit.ui.PropertyRegistry import UI_PROPERTY_REGISTRY
from duit.ui.annotations.BooleanAnnotation import BooleanAnnotation
from duit.ui.wx.properties.BooleanProperty import BooleanProperty


def init_wx_registry():
    UI_PROPERTY_REGISTRY[BooleanAnnotation] = BooleanProperty
