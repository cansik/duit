# Duit (Data UI Toolkit)

[![Documentation](https://img.shields.io/badge/read-documentation-blue)](https://cansik.github.io/duit/)
[![Duit Test](https://github.com/cansik/duit/actions/workflows/test.yml/badge.svg)](https://github.com/cansik/duit/actions/workflows/test.yml)
[![PyPI](https://img.shields.io/pypi/v/duit)](https://pypi.org/project/duit/)
[![Github](https://img.shields.io/badge/github-duit-green.svg?logo=github)](https://github.com/cansik/duit)

Duit is a Python library that provides a set of tools for working with data in a structured and efficient way. The goal
of duit is to make it easy for developers to create and manage data models and create simple user interfaces for
data entry and display. The implementation is based on the ideas
of [cansik/bildspur-base](https://github.com/cansik/bildspur-base)
and [cansik/bildspur-ui](https://github.com/cansik/bildspur-ui).

<img width="800" alt="gui-demo" src="./doc/gui-demo.png">

*Example UI rendered with [NiceGUI](https://nicegui.io/) [Open3D](https://github.com/isl-org/Open3D), [tkinter](https://docs.python.org/3/library/tkinter.html) and [wx](https://pypi.org/project/wxPython/) (ltr)*.

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
pip install duit
```

To support user interface creation for data fields, one of the following backends can be installed:

- [open3d](https://github.com/isl-org/Open3D) - Cross platform UI framework with support for 3d visualisation.
- [wx](https://pypi.org/project/wxPython/) - Wx based UI framework which is cross platfrom and very stable.
- [nicegui](https://nicegui.io/) - Web based interface which looks really nice and is our favourite choice.
- [tkinter](https://docs.python.org/3/library/tkinter.html) - More stable UI framework, currently not feature complete.

If you are already using `open3d`, this is the recommended choice as gui backend.

```bash
pip install "duit[open3d]"
```

To install `tkinter` use the following command:

```bash
pip install "duit[tk]"
```

To install `wx` use the following command:

```bash
pip install "duit[wx]"
```

To install `nicegui` use the following command:

```bash
pip install "duit[nicegui]"
```

To install duit with all backends call pip like this:

```bash
pip install "duit[all]"
```

## Example

This is a very basic example on how to use `duit`. Read to [documentation](https://cansik.github.io/duit/duit.html#documentation) for a more information about the core concepts.

```python
import argparse

from open3d.visualization import gui

from duit import ui
from duit.arguments.Argument import Argument
from duit.arguments.Arguments import DefaultArguments
from duit.model.DataField import DataField
from duit.settings.Settings import DefaultSettings
from duit.ui.ContainerHelper import ContainerHelper
from duit.ui.open3d.Open3dPropertyPanel import Open3dPropertyPanel
from duit.ui.open3d.Open3dPropertyRegistry import init_open3d_registry


class Config:
    def __init__(self):
        container_helper = ContainerHelper(self)

        with container_helper.section("User"):
            self.name = DataField("Cat") | ui.Text("Name")
            self.age = DataField(21) | ui.Slider("Age", limit_min=18, limit_max=99)

        with container_helper.section("Application"):
            self.enabled = DataField(True) | ui.Boolean("Enabled") | Argument()


def main():
    # create initial config
    config = Config()

    # register a custom listener for the enabled flag
    config.enabled.on_changed += lambda e: print(f"Enabled: {e}")

    # add arguments and parse
    parser = argparse.ArgumentParser()
    args = DefaultArguments.add_and_configure(parser, config)

    # store current config
    DefaultSettings.save("config.json", config)

    # create open3d gui for to display config
    init_open3d_registry()

    app = gui.Application.instance
    app.initialize()

    window: gui.Window = gui.Application.instance.create_window("Demo Window", 400, 200)
    panel = Open3dPropertyPanel(window)
    window.add_child(panel)
    panel.data_context = config

    app.run()


if __name__ == "__main__":
    main()
```

Which results in the following GUI.

<img width="480" alt="example-window" src="./doc/example-window.png">

### Development

To develop it is recommended to clone this repository and install the dependencies like this:

```bash
# in the duit directory
pip install -e ".[all]"
```

#### Generate Documentation

```bash
# create documentation into "./docs
python setup.py doc

# launch pdoc webserver
python setup.py doc --launch
```

## About

MIT License - Copyright (c) 2025 Florian Bruggisser
