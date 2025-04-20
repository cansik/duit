from duit.ui.PropertyRegistry import UI_PROPERTY_REGISTRY
from duit.ui.annotations.TextAnnotation import TextAnnotation
from duit.ui.nicegui.properties.TextProperty import TextProperty


def init_nicegui_registry():
    """
    Initialize the NiceGUI property registry with mappings between UI annotations and NiceGUI property classes.
    This allows NiceGUI widgets to be created based on the UI annotations used in data models.

    """
    UI_PROPERTY_REGISTRY[TextAnnotation] = TextProperty
