from duit.ui.PropertyRegistry import UI_PROPERTY_REGISTRY
from duit.ui.annotations import NumberAnnotation
from duit.ui.annotations.ActionAnnotation import ActionAnnotation
from duit.ui.annotations.BooleanAnnotation import BooleanAnnotation
from duit.ui.annotations.EnumAnnotation import EnumAnnotation
from duit.ui.annotations.ListAnnotation import ListAnnotation
from duit.ui.annotations.OptionsAnnotation import OptionsAnnotation
from duit.ui.annotations.PathAnnotation import PathAnnotation
from duit.ui.annotations.ProgressAnnotation import ProgressAnnotation
from duit.ui.annotations.SliderAnnotation import SliderAnnotation
from duit.ui.annotations.TextAnnotation import TextAnnotation
from duit.ui.annotations.TitleAnnoation import TitleAnnotation
from duit.ui.annotations.VectorAnnotation import VectorAnnotation
from duit.ui.wx.properties.ActionProperty import ActionProperty
from duit.ui.wx.properties.ListProperty import ListProperty
from duit.ui.wx.properties.PathProperty import PathProperty
from duit.ui.wx.properties.BooleanProperty import BooleanProperty
from duit.ui.wx.properties.EnumProperty import EnumProperty
from duit.ui.wx.properties.NumberProperty import NumberProperty
from duit.ui.wx.properties.OptionsProperty import OptionsProperty
from duit.ui.wx.properties.ProgressProperty import ProgressProperty
from duit.ui.wx.properties.SliderProperty import SliderProperty
from duit.ui.wx.properties.TextProperty import TextProperty
from duit.ui.wx.properties.VectorProperty import VectorProperty
from duit.ui.wx.properties.TitleProperty import TitleProperty


def init_wx_registry():
    UI_PROPERTY_REGISTRY[BooleanAnnotation] = BooleanProperty
    UI_PROPERTY_REGISTRY[TextAnnotation] = TextProperty
    UI_PROPERTY_REGISTRY[NumberAnnotation] = NumberProperty
    UI_PROPERTY_REGISTRY[SliderAnnotation] = SliderProperty
    UI_PROPERTY_REGISTRY[ProgressAnnotation] = ProgressProperty
    UI_PROPERTY_REGISTRY[OptionsAnnotation] = OptionsProperty
    UI_PROPERTY_REGISTRY[EnumAnnotation] = EnumProperty
    UI_PROPERTY_REGISTRY[PathAnnotation] = PathProperty
    UI_PROPERTY_REGISTRY[VectorAnnotation] = VectorProperty
    UI_PROPERTY_REGISTRY[ActionAnnotation] = ActionProperty
    UI_PROPERTY_REGISTRY[ListAnnotation] = ListProperty
    UI_PROPERTY_REGISTRY[TitleAnnotation] = TitleProperty
