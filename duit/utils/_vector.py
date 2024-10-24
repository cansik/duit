from typing import Sequence

import vector


def get_vector_attributes(value: vector.Vector) -> Sequence[str]:
    """
    Get the attribute names (components) of a `vector.Vector` object.

    Args:
        value (vector.Vector): The `vector.Vector` object to retrieve the attributes from.

    Returns:
        Sequence[str]: A sequence of attribute names (e.g., "x", "y", "z", "t") for the given vector.

    Raises:
        None
    """
    if isinstance(value, vector.Vector2D):
        return "x", "y"
    elif isinstance(value, vector.Vector3D):
        return "x", "y", "z"
    elif isinstance(value, vector.Vector4D):
        return "x", "y", "z", "t"
