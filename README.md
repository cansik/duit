# Simbi
Simbi is a toolkit with helpful code for python.

It is based on the ideas of [cansik/bildspur-base](https://github.com/cansik/bildspur-base) and [cansik/bildspur-ui](https://github.com/cansik/bildspur-ui).

## Example

To create a gui by code, create a new class with the fields you need.

```python
class Config:
    def __init__(self):
        self.age = DataField(5) | NumberAnnotation("Age")
        self.hungry = DataField(True) | BooleanAnnotation("Hungry")
        self.year = DataField(2021) | NumberAnnotation("Year", 2000, 2050)
        self.temperature = DataField(30.2) | SliderAnnotation("Temperature", 0, 40)
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

## Installation
To install simbi with all dependencies call pip like this:

```bash
pip install "simbi[all]"
```

It is also possible to only install certain packages (for example for the open3d gui):

```bash
pip install "simbi[open3d]"
```

### Development

To develop it is recommended to clone this repository and install the dependencies like this:

```bash
# in the simbi directory
pip install -e ".[all]"
```

## About
Copyright (c) 2022 Florian Bruggisser