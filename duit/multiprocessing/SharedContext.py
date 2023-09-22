from typing import Any, Optional
import multiprocessing as mp


class SharedContext:
    def __init__(self, obj: Any, manager: Optional[mp.Manager] = None):
        self.manager = manager if manager is not None else mp.Manager()

        # for each field create a Value
        # add on changed handlers to update value
        # future: add thread to signal with other managers to propagate changes
