from typing import Dict, Type

from duit.ui.BaseProperty import BaseProperty
from duit.ui.annotations import UIAnnotation

# Dictionary that maps UIAnnotation types to BaseProperty types.
UI_PROPERTY_REGISTRY: Dict[Type[UIAnnotation], Type[BaseProperty]] = {}
