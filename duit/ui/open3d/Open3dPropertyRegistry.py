from duit.ui.PropertyRegistry import UI_PROPERTY_REGISTRY
from duit.ui.annotations import NumberAnnotation
from duit.ui.annotations.ActionAnnotation import ActionAnnotation
from duit.ui.annotations.BooleanAnnotation import BooleanAnnotation
from duit.ui.annotations.EnumAnnotation import EnumAnnotation
from duit.ui.annotations.OptionsAnnotation import OptionsAnnotation
from duit.ui.annotations.PathAnnotation import PathAnnotation
from duit.ui.annotations.SliderAnnotation import SliderAnnotation
from duit.ui.annotations.TextAnnotation import TextAnnotation
from duit.ui.annotations.VectorAnnotation import VectorAnnotation
from duit.ui.open3d.properties.ActionProperty import ActionProperty
from duit.ui.open3d.properties.EnumProperty import EnumProperty
from duit.ui.open3d.properties.OptionsProperty import OptionsProperty
from duit.ui.open3d.properties.BooleanProperty import BooleanProperty
from duit.ui.open3d.properties.NumberProperty import NumberProperty
from duit.ui.open3d.properties.PathProperty import PathProperty
from duit.ui.open3d.properties.SliderProperty import SliderProperty
from duit.ui.open3d.properties.TextProperty import TextProperty
from duit.ui.open3d.properties.VectorProperty import VectorProperty


def init_open3d_registry():
    UI_PROPERTY_REGISTRY[NumberAnnotation] = NumberProperty
    UI_PROPERTY_REGISTRY[BooleanAnnotation] = BooleanProperty
    UI_PROPERTY_REGISTRY[SliderAnnotation] = SliderProperty
    UI_PROPERTY_REGISTRY[OptionsAnnotation] = OptionsProperty
    UI_PROPERTY_REGISTRY[EnumAnnotation] = EnumProperty
    UI_PROPERTY_REGISTRY[TextAnnotation] = TextProperty
    UI_PROPERTY_REGISTRY[ActionAnnotation] = ActionProperty
    UI_PROPERTY_REGISTRY[VectorAnnotation] = VectorProperty
    UI_PROPERTY_REGISTRY[PathAnnotation] = PathProperty
