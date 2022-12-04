from duit.ui.PropertyRegistry import UI_PROPERTY_REGISTRY
from duit.ui.annotations import NumberAnnotation
from duit.ui.annotations.ActionAnnotation import ActionAnnotation
from duit.ui.annotations.BooleanAnnotation import BooleanAnnotation
from duit.ui.annotations.EnumAnnotation import EnumAnnotation
from duit.ui.annotations.OptionsAnnotation import OptionsAnnotation
from duit.ui.annotations.SliderAnnotation import SliderAnnotation
from duit.ui.tk.properties.ActionProperty import ActionProperty
from duit.ui.tk.properties.BooleanProperty import BooleanProperty
from duit.ui.tk.properties.EnumProperty import EnumProperty
from duit.ui.tk.properties.NumberProperty import NumberProperty
from duit.ui.tk.properties.OptionsProperty import OptionsProperty
from duit.ui.tk.properties.SliderProperty import SliderProperty


def init_tk_registry():
    UI_PROPERTY_REGISTRY[NumberAnnotation] = NumberProperty
    UI_PROPERTY_REGISTRY[BooleanAnnotation] = BooleanProperty
    UI_PROPERTY_REGISTRY[ActionAnnotation] = ActionProperty
    UI_PROPERTY_REGISTRY[OptionsAnnotation] = OptionsProperty
    UI_PROPERTY_REGISTRY[EnumAnnotation] = EnumProperty
    UI_PROPERTY_REGISTRY[SliderAnnotation] = SliderProperty
