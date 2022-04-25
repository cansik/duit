# Simbi [![PyPI](https://img.shields.io/pypi/v/simbi)](https://pypi.org/project/simbi/)
Simbi is a toolkit to create simple user-interfaces for python.

It is based on the ideas of [cansik/bildspur-base](https://github.com/cansik/bildspur-base) and [cansik/bildspur-ui](https://github.com/cansik/bildspur-ui).

## Installation
To install simbi with all dependencies call pip like this:

```bash
pip install "simbi[all]"
```

It is also possible to only install certain packages (for example for the open3d gui):

```bash
pip install "simbi[open3d]"
```

## Example

To create a gui by code, create a new class with the data-fields you need.

```python
from examples.Color import Color
from simbi.model.DataField import DataField
import simbi.ui as ui

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
To save and load settings have a look at the following example. Serialization from and to `json` is automatically handled by simbi.

```python
config = Config()
settings = Settings()

settings.save("test.json", config)
settings.load("test.json", config)
```

### Development

To develop it is recommended to clone this repository and install the dependencies like this:

```bash
# in the simbi directory
pip install -e ".[all]"
```

## About
MIT License - Copyright (c) 2022 Florian Bruggisser