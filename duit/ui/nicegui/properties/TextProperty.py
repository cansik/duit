from nicegui import ui
from nicegui.element import Element

from duit.model.DataField import DataField
from duit.ui.annotations.TextAnnotation import TextAnnotation
from duit.ui.nicegui.NiceGUIFieldProperty import NiceGUIFieldProperty


class TextProperty(NiceGUIFieldProperty[TextAnnotation, DataField]):
    def create_field(self) -> Element:
        return ui.input()
