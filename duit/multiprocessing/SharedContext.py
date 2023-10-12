from typing import Any, Optional
import multiprocessing as mp

from duit.annotation.AnnotationFinder import AnnotationFinder
from duit.model.DataField import DataField
from duit.multiprocessing.Shared import Shared


class SharedContext:
    def __init__(self, obj: Any, manager: Optional[mp.Manager] = None):
        self.manager: mp.Manager = manager if manager is not None else mp.Manager()

        # for each field create a Value
        # add on changed handlers to update value
        # future: add thread to signal with other managers to propagate changes

        self._attach_to_obj(obj)

    def close(self):
        self.manager.close()

    def _attach_to_obj(self, obj: Any):
        def _is_field_valid(field: DataField, _: Shared):
            if callable(field.value):
                return False
            return True

        finder = AnnotationFinder(Shared, _is_field_valid, recursive=True)

        for name, (field, annotation) in finder.find(obj).items():
            print(name)
