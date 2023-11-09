# Duit (Data UI Toolkit)

[![Documentation](https://img.shields.io/badge/read-documentation-blue)](https://cansik.github.io/duit/)
[![PyPI](https://img.shields.io/pypi/v/duit)](https://pypi.org/project/duit/)

Duit is a Python library that provides a set of tools for working with data in a structured and efficient way. The goal
of duit is to make it easy for developers to create and manage complex data models and create simple user interfaces for
data entry and display. The implementation is based on the ideas
of [cansik/bildspur-base](https://github.com/cansik/bildspur-base)
and [cansik/bildspur-ui](https://github.com/cansik/bildspur-ui).

<img width="200" alt="python_1xlGn4l6Pb" src="https://user-images.githubusercontent.com/5220162/165138252-d7ac7542-974a-4573-ba88-35724e94b0d8.png">

*Example UI rendered with [Open3D](https://github.com/isl-org/Open3D)*

## Features

- **Data Modeling**: duit provides a flexible data modeling framework to create structured data models and fields.

- **Annotations**: Use annotations to attach metadata to data fields, making it easier to work with them.

- **Command-line Arguments**: Easily parse and configure command-line arguments in your applications based on data
  fields.

- **Settings Serialization**: Serialize and deserialize settings from data fields to and from json.

- **User Interface**: Create simple user-interfaces for data fields.

## Installation

By default, only the data modeling, annotation, arguments and settings modules are installed.

```bash
pip install "duit"
```

To support user interface creation for data fields, one of the following backends can be installed:

- [open3d](https://github.com/isl-org/Open3D) - Cross platform UI framework with support for 3d visualisation.
- [tkinter](https://docs.python.org/3/library/tkinter.html) - More stable UI framework, currently not feature complete.

At the moment `open3d` is the recommended choice as gui backend.

```bash
pip install "duit[open3d]"
```

To install `tkinter` use the following command:

```bash
pip install "duit[tkinter]"
```

To install duit with all backends call pip like this:

```bash
pip install "duit[all]"
```

## Example

To create a gui by code, create a new class with the data-fields you need.

```python
from examples.Color import Color
from duit.model.DataField import DataField
import duit.ui as ui


class Config:
    def __init__(self):
        self.hungry = DataField(True) | ui.Boolean("Hungry")
        self.year = DataField(2021) | ui.Number("Year", 2000, 2050)
        self.temperature = DataField(30.2) | ui.Slider("Temperature", 0, 40)
        self.resolution = DataField(256) | ui.Options("Resolution", [64, 128, 256, 512, 1024])
        self.color = DataField(Color.White) | ui.Enum("Color")
        self.name = DataField("Test") | ui.Text("Name", readonly=True)
```

And use the open3d gui package to display them:

```python
init_open3d_registry()

config = Config()
config.age.value = 10

app = o3d.visualization.gui.Application.instance
app.initialize()

win = DemoWindow(config)

app.run()
```

## Settings

To save and load settings have a look at the following example. Serialization from and to `json` is automatically
handled by duit.

```python
config = Config()
settings = Settings()

settings.save("test.json", config)
settings.load("test.json", config)
```

### Development

To develop it is recommended to clone this repository and install the dependencies like this:

```bash
# in the duit directory
pip install -e ".[all]"
```

## About

MIT License - Copyright (c) 2023 Florian Bruggisser