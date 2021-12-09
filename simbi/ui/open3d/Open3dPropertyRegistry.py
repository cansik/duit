from simbi.ui.PropertyRegistry import UI_PROPERTY_REGISTRY
from simbi.ui.annotations import NumberAnnotation
from simbi.ui.annotations.BooleanAnnotation import BooleanAnnotation
from simbi.ui.annotations.OptionsAnnotation import OptionsAnnotation
from simbi.ui.annotations.SliderAnnotation import SliderAnnotation
from simbi.ui.open3d.properties.OptionsProperty import OptionsProperty
from simbi.ui.open3d.properties.BooleanProperty import BooleanProperty
from simbi.ui.open3d.properties.NumberProperty import NumberProperty
from simbi.ui.open3d.properties.SliderProperty import SliderProperty


def init_open3d_registry():
    UI_PROPERTY_REGISTRY[NumberAnnotation] = NumberProperty
    UI_PROPERTY_REGISTRY[BooleanAnnotation] = BooleanProperty
    UI_PROPERTY_REGISTRY[SliderAnnotation] = SliderProperty
    UI_PROPERTY_REGISTRY[OptionsAnnotation] = OptionsProperty
