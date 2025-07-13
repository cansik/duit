from __future__ import annotations

from dataclasses import dataclass, field

from duit.model.DataField import DataField
from duit.ui.annotations import UIAnnotation


@dataclass
class MetaNode:
    """
    A generic node in the property tree.
    - If annotation is a StartSection or SubSection, children holds nested nodes.
    - Otherwise it's a leaf for a single field.
    """
    name: str
    annotation: UIAnnotation
    model: DataField | None = None
    children: list[MetaNode] = field(default_factory=list)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"MetaNode({self.name}, {type(self.annotation).__name__}"
