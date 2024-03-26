from duit.ui.PropertyRegistry import UI_PROPERTY_REGISTRY
from duit.ui.annotations import NumberAnnotation
from duit.ui.annotations.BooleanAnnotation import BooleanAnnotation
from duit.ui.annotations.SliderAnnotation import SliderAnnotation
from duit.ui.annotations.TextAnnotation import TextAnnotation
from duit.ui.wx.properties.BooleanProperty import BooleanProperty
from duit.ui.wx.properties.NumberProperty import NumberProperty
from duit.ui.wx.properties.SliderProperty import SliderProperty
from duit.ui.wx.properties.TextProperty import TextProperty


def init_wx_registry():
    UI_PROPERTY_REGISTRY[BooleanAnnotation] = BooleanProperty
    UI_PROPERTY_REGISTRY[TextAnnotation] = TextProperty
    UI_PROPERTY_REGISTRY[NumberAnnotation] = NumberProperty
    UI_PROPERTY_REGISTRY[SliderAnnotation] = SliderProperty
