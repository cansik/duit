import argparse

from duit.arguments.Argument import Argument
from duit.arguments.Arguments import DefaultArguments
from duit.model.DataField import DataField


class Config:
    def __init__(self):
        self.device = DataField(0) | Argument(help="Device id.")
        self.write_output = DataField(False) | Argument(help="Write output to console.")
        self.debug_text = DataField("123") | Argument(dest="--dbg", help="Debug text.")


config = Config()

# create argument parser and automatically add and configure the config class
parser = argparse.ArgumentParser()
args = DefaultArguments.add_and_configure(parser, config)