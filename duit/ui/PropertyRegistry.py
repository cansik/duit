from typing import Dict, Type

from duit.ui.BaseProperty import BaseProperty
from duit.ui.annotations import UIAnnotation

UI_PROPERTY_REGISTRY: Dict[Type[UIAnnotation], Type[BaseProperty]] = {}
