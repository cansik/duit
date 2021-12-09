from typing import Dict, Type

from simbi.ui.BaseProperty import BaseProperty
from simbi.ui.annotations import UIAnnotation

UI_PROPERTY_REGISTRY: Dict[Type[UIAnnotation], Type[BaseProperty]] = {}
