from typing import Sequence

import vector


def get_vector_attributes(value: vector.Vector) -> Sequence[str]:
    if isinstance(value, vector.Vector2D):
        return "x", "y"
    elif isinstance(value, vector.Vector3D):
        return "x", "y", "z"
    elif isinstance(value, vector.Vector4D):
        return "x", "y", "z", "t"
