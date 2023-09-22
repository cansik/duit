import multiprocessing as mp
import time
from enum import Enum
from typing import Optional

import numpy as np

from duit.model.DataField import DataField
from duit.model.SharedDataField import SharedDataField
from duit.multiprocessing.Shared import Shared
from duit.multiprocessing.SharedContext import SharedContext


class Day(Enum):
    Today = 1,
    Tomorrow = 2


class Config:
    def __init__(self, manager: mp.Manager):
        self.counter = DataField(0) | Shared()
        self.data = SharedDataField(np.ones((2,)), manager)
        self.day = SharedDataField(Day.Today, manager)


class ValueHandler:
    def __init__(self, config: Config):
        self.config = config

        self.process: Optional[mp.Process] = None
        self._exit_flag: Optional[mp.Event] = None

    def run(self):
        self._exit_flag = mp.Event()
        self.process = mp.Process(target=self._loop)
        self.process.start()

    def stop(self):
        self._exit_flag.set()
        self.process.join(5)

    def _loop(self):
        result = self.config.data.value * 23
        self.config.data.value = result

        while not self._exit_flag.is_set():
            print(f"still running => {self.config.counter.value}")
            self.config.counter.value += 1
            time.sleep(0.25)

        print(self.config.data.value)
        self.config.day.value = Day.Tomorrow


def main():
    # create manager
    manager = mp.Manager()

    config = Config(manager)
    config.counter.value = 42

    context = SharedContext(config, manager)

    handler = ValueHandler(config)
    handler.run()

    time.sleep(1)

    handler.stop()

    print(config.counter.value)
    print(config.data.value)
    print(config.day.value)


if __name__ == "__main__":
    main()
