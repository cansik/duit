from simbi.ui.PropertyRegistry import UI_PROPERTY_REGISTRY
from simbi.ui.annotations import NumberAnnotation
from simbi.ui.annotations.ActionAnnotation import ActionAnnotation
from simbi.ui.annotations.BooleanAnnotation import BooleanAnnotation
from simbi.ui.annotations.EnumAnnotation import EnumAnnotation
from simbi.ui.annotations.OptionsAnnotation import OptionsAnnotation
from simbi.ui.annotations.SliderAnnotation import SliderAnnotation
from simbi.ui.annotations.TextAnnotation import TextAnnotation
from simbi.ui.open3d.properties.ActionProperty import ActionProperty
from simbi.ui.open3d.properties.EnumProperty import EnumProperty
from simbi.ui.open3d.properties.OptionsProperty import OptionsProperty
from simbi.ui.open3d.properties.BooleanProperty import BooleanProperty
from simbi.ui.open3d.properties.NumberProperty import NumberProperty
from simbi.ui.open3d.properties.SliderProperty import SliderProperty
from simbi.ui.open3d.properties.TextProperty import TextProperty


def init_open3d_registry():
    UI_PROPERTY_REGISTRY[NumberAnnotation] = NumberProperty
    UI_PROPERTY_REGISTRY[BooleanAnnotation] = BooleanProperty
    UI_PROPERTY_REGISTRY[SliderAnnotation] = SliderProperty
    UI_PROPERTY_REGISTRY[OptionsAnnotation] = OptionsProperty
    UI_PROPERTY_REGISTRY[EnumAnnotation] = EnumProperty
    UI_PROPERTY_REGISTRY[TextAnnotation] = TextProperty
    UI_PROPERTY_REGISTRY[ActionAnnotation] = ActionProperty
