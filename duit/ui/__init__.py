from .annotations.ActionAnnotation import ActionAnnotation as Action
from .annotations.BooleanAnnotation import BooleanAnnotation as Boolean
from .annotations.EnumAnnotation import EnumAnnotation as Enum
from .annotations.ListAnnotation import ListAnnotation as List
from .annotations.NumberAnnotation import NumberAnnotation as Number
from .annotations.OptionsAnnotation import OptionsAnnotation as Options
from .annotations.PathAnnotation import PathAnnotation as Path
from .annotations.ProgressAnnotation import ProgressAnnotation as Progress
from .annotations.SliderAnnotation import SliderAnnotation as Slider
from .annotations.TextAnnotation import TextAnnotation as Text
from .annotations.VectorAnnotation import VectorAnnotation as Vector
from .annotations.TitleAnnoation import TitleAnnotation as Title
from .annotations.container.EndSectionAnnotation import EndSectionAnnotation as EndSection
from .annotations.container.StartSectionAnnotation import StartSectionAnnotation as StartSection
from .annotations.container.SubSectionAnnotation import SubSectionAnnotation as SubSection


def setup_open3d():
    """
    Set up Open3D-specific annotations and properties.

    This function initializes Open3D-specific annotation and property types.

    Note: This function is part of the Open3D integration and should be called if Open3D-specific
    functionality is used.

    """
    from .open3d.Open3dPropertyRegistry import init_open3d_registry
    init_open3d_registry()


def setup_tk():
    """
    Set up Tkinter-specific annotations and properties.

    This function is a placeholder for setting up Tkinter-specific annotation and property types.
    """
    pass
