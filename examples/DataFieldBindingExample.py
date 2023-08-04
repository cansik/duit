from duit.model.DataField import DataField
from duit.utils.name_reference import create_name_reference


class Example:
    def __init__(self):
        self.time = 5


obj = Example()
field = DataField(25)

field.bind_to_attribute(obj, create_name_reference(obj).time)
field.value = 30

print(f"Value: {obj.time}")
