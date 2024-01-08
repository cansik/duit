from duit.ui.PropertyRegistry import UI_PROPERTY_REGISTRY
from duit.ui.annotations import NumberAnnotation
from duit.ui.annotations.ActionAnnotation import ActionAnnotation
from duit.ui.annotations.BooleanAnnotation import BooleanAnnotation
from duit.ui.annotations.EnumAnnotation import EnumAnnotation
from duit.ui.annotations.OptionsAnnotation import OptionsAnnotation
from duit.ui.annotations.ProgressAnnotation import ProgressAnnotation
from duit.ui.annotations.SliderAnnotation import SliderAnnotation
from duit.ui.annotations.TextAnnotation import TextAnnotation
from duit.ui.annotations.VectorAnnotation import VectorAnnotation
from duit.ui.tk.properties.ActionProperty import ActionProperty
from duit.ui.tk.properties.BooleanProperty import BooleanProperty
from duit.ui.tk.properties.EnumProperty import EnumProperty
from duit.ui.tk.properties.NumberProperty import NumberProperty
from duit.ui.tk.properties.OptionsProperty import OptionsProperty
from duit.ui.tk.properties.ProgressProperty import ProgressProperty
from duit.ui.tk.properties.SliderProperty import SliderProperty
from duit.ui.tk.properties.TextProperty import TextProperty
from duit.ui.tk.properties.VectorProperty import VectorProperty


def init_tk_registry():
    """
    Initialize the Tk property registry with mapping between annotation types and their respective property classes.
    """
    UI_PROPERTY_REGISTRY[NumberAnnotation] = NumberProperty
    UI_PROPERTY_REGISTRY[BooleanAnnotation] = BooleanProperty
    UI_PROPERTY_REGISTRY[ActionAnnotation] = ActionProperty
    UI_PROPERTY_REGISTRY[OptionsAnnotation] = OptionsProperty
    UI_PROPERTY_REGISTRY[EnumAnnotation] = EnumProperty
    UI_PROPERTY_REGISTRY[SliderAnnotation] = SliderProperty
    UI_PROPERTY_REGISTRY[TextAnnotation] = TextProperty
    UI_PROPERTY_REGISTRY[VectorAnnotation] = VectorProperty
    UI_PROPERTY_REGISTRY[ProgressAnnotation] = ProgressProperty
