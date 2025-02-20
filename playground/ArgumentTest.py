import argparse
from enum import Enum

import vector

from duit.arguments.Argument import Argument
from duit.arguments.Arguments import DefaultArguments
from duit.model.DataField import DataField


class Mood(Enum):
    Happy = 0
    Sad = 1
    Sunny = 2


class Location:
    def __init__(self):
        self.position = DataField(vector.obj(x=100, y=50)) | Argument()
        self.name = DataField("Markus") | Argument()


class Config:
    def __init__(self):
        self.name = DataField("Florian") | Argument()
        self.device = DataField(0) | Argument(help="Device id.")
        self.write_output = DataField(False) | Argument(help="Write output to console.")
        self.debug_text = DataField("123") | Argument(dest="--dbg", help="Debug text.")
        self.mood = DataField(Mood.Happy) | Argument()
        self.rotation = DataField(vector.obj(x=2, y=3)) | Argument(auto_default=True)

        self.location = DataField(Location())


config = Config()

# create argument parser and automatically add and configure the config class
parser = argparse.ArgumentParser()
DefaultArguments.add_arguments(parser, config, use_attribute_path_as_name=True)

config.device.value = 1
config.mood.value = Mood.Sunny
config.rotation.value = vector.obj(x=5, y=10)

args = parser.parse_args()
DefaultArguments.configure(args, config)

print(config.name)
print(config.device)
print(config.write_output)
print(config.debug_text)
print(config.mood)
print(config.rotation)
print(config.location.value.name)
