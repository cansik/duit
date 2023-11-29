from duit.iterator.AnnotationIterator import AnnotationIterator
from duit.model.DataField import DataField


class Config:
    def __init__(self):
        self.a = DataField("A")
        self.b = DataField("B")
        self.c = DataField("C")


def main():
    config = Config()

    for field in AnnotationIterator(config):
        print(f"{field.parent_field_name}: {field.parent} - Ann: {field.field_value}")


if __name__ == "__main__":
    main()
