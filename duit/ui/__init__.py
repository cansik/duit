from .annotations.ActionAnnotation import ActionAnnotation as Action
from .annotations.BooleanAnnotation import BooleanAnnotation as Boolean
from .annotations.EnumAnnotation import EnumAnnotation as Enum
from .annotations.NumberAnnotation import NumberAnnotation as Number
from .annotations.OptionsAnnotation import OptionsAnnotation as Options
from .annotations.SliderAnnotation import SliderAnnotation as Slider
from .annotations.TextAnnotation import TextAnnotation as Text
from .annotations.VectorAnnotation import VectorAnnotation as Vector
from .annotations.PathAnnotation import PathAnnotation as Path

from .annotations.container.StartSectionAnnotation import StartSectionAnnotation as StartSection
from .annotations.container.EndSectionAnnotation import EndSectionAnnotation as EndSection
from .annotations.container.SubSectionAnnotation import SubSectionAnnotation as SubSection


def setup_open3d():
    from .open3d.Open3dPropertyRegistry import init_open3d_registry
    init_open3d_registry()


def setup_tk():
    pass
