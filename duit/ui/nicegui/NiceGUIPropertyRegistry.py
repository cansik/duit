from duit.ui.PropertyRegistry import UI_PROPERTY_REGISTRY
from duit.ui.annotations.ActionAnnotation import ActionAnnotation
from duit.ui.annotations.BooleanAnnotation import BooleanAnnotation
from duit.ui.annotations.EnumAnnotation import EnumAnnotation
from duit.ui.annotations.ListAnnotation import ListAnnotation
from duit.ui.annotations.NumberAnnotation import NumberAnnotation
from duit.ui.annotations.OptionsAnnotation import OptionsAnnotation
from duit.ui.annotations.PathAnnotation import PathAnnotation
from duit.ui.annotations.ProgressAnnotation import ProgressAnnotation
from duit.ui.annotations.SliderAnnotation import SliderAnnotation
from duit.ui.annotations.TextAnnotation import TextAnnotation
from duit.ui.annotations.TitleAnnoation import TitleAnnotation
from duit.ui.annotations.VectorAnnotation import VectorAnnotation
from duit.ui.nicegui.properties.ActionProperty import ActionProperty
from duit.ui.nicegui.properties.BooleanProperty import BooleanProperty
from duit.ui.nicegui.properties.EnumProperty import EnumProperty
from duit.ui.nicegui.properties.ListProperty import ListProperty
from duit.ui.nicegui.properties.NumberProperty import NumberProperty
from duit.ui.nicegui.properties.OptionsProperty import OptionsProperty
from duit.ui.nicegui.properties.PathProperty import PathProperty
from duit.ui.nicegui.properties.ProgressProperty import ProgressProperty
from duit.ui.nicegui.properties.SliderAnnotation import SliderProperty
from duit.ui.nicegui.properties.TextProperty import TextProperty
from duit.ui.nicegui.properties.TitleProperty import TitleProperty
from duit.ui.nicegui.properties.VectorProperty import VectorProperty


def init_nicegui_registry():
    """
    Initialize the NiceGUI property registry with mappings between UI annotations and NiceGUI property classes.
    This allows NiceGUI widgets to be created based on the UI annotations used in data models.

    """
    UI_PROPERTY_REGISTRY[TextAnnotation] = TextProperty
    UI_PROPERTY_REGISTRY[BooleanAnnotation] = BooleanProperty
    UI_PROPERTY_REGISTRY[ActionAnnotation] = ActionProperty
    UI_PROPERTY_REGISTRY[NumberAnnotation] = NumberProperty
    UI_PROPERTY_REGISTRY[ListAnnotation] = ListProperty
    UI_PROPERTY_REGISTRY[OptionsAnnotation] = OptionsProperty
    UI_PROPERTY_REGISTRY[EnumAnnotation] = EnumProperty
    UI_PROPERTY_REGISTRY[PathAnnotation] = PathProperty
    UI_PROPERTY_REGISTRY[ProgressAnnotation] = ProgressProperty
    UI_PROPERTY_REGISTRY[TitleAnnotation] = TitleProperty
    UI_PROPERTY_REGISTRY[SliderAnnotation] = SliderProperty
    UI_PROPERTY_REGISTRY[VectorAnnotation] = VectorProperty
