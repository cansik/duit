import time

from duit.iterator.DataFieldIterator import DataFieldIterator
from duit.model.DataField import DataField


class Config:
    def __init__(self):
        self.a = DataField("A")
        self.b = DataField("B")
        self.c = DataField("C")

        self.z = SubConfig()


class SubConfig:
    def __init__(self):
        self.z = DataField("Z")


def main():
    config = Config()

    start = time.time()
    for field in DataFieldIterator(config):
        print(field.field_name)
    end = time.time()
    print(f"Time: {(end - start) * 1000:.2f}ms")


if __name__ == "__main__":
    main()
