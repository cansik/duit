# User Interface

`duit` can automatically create simple user interfaces from data models. A  
property panel shows every `DataField` of an object as a widget and keeps the  
values in sync. The GUI system is backend agnostic so the same configuration can  
be displayed with different frameworks.

## Backends

Different GUI backends are supported. A backend needs to be installed with the  
corresponding extra and the property registry has to be initialised.

- **Open3D** – desktop GUI based on `open3d.visualization.gui` with strong 3D  
  integration.  
- **Tkinter** – lightweight UI using the Python standard library.  
- **wx** – mature cross platform UI built on wxPython.  
- **NiceGUI** – browser based interface powered by NiceGUI.

```bash
pip install "duit[open3d]"  # Open3D
pip install "duit[tk]"      # tkinter
pip install "duit[wx]"      # wx
pip install "duit[nicegui]" # NiceGUI
````

Once installed the backend registry must be initialised before creating a
property panel.

## Creating a Property Panel

A property panel renders all annotated fields of a configuration. Each backend
implements its own version of
`duit.ui.BasePropertyPanel.BasePropertyPanel`. Before a panel can be created the
backend specific property registry has to be initialised so that the
annotations are mapped to widgets. Afterwards the GUI application is started,
a window is created and the panel is attached to it.

```python
from open3d.visualization import gui
from duit.ui.open3d.Open3dPropertyPanel import Open3dPropertyPanel
from duit.ui.open3d.Open3dPropertyRegistry import init_open3d_registry

init_open3d_registry()                                   # 1. prepare widgets
app = gui.Application.instance                          # 2. create app
app.initialize()
window = gui.Application.instance.create_window("Demo", 400, 200)  # 3. window
panel = Open3dPropertyPanel(window)                     # 4. property panel
window.add_child(panel)
panel.data_context = config                             # 5. connect config
app.run()                                               # 6. start gui
```

## UI Annotations

Annotations describe how a `DataField` should be rendered. Multiple annotations
can be applied to the same field. Each annotation accepts `name`, `tooltip` and
`readonly` arguments. Widgets are arranged in a two column layout, using
the provided `name` as the label. The annotations are available from the
`duit.ui` module.

* `Number` – numeric value input.
* `Slider` – slider widget for numeric values.
* `Boolean` – check box or switch for boolean values.
* `Text` – text entry field.
* `Options` – drop down list with selectable options.
* `Enum` – options based on an enum type.
* `Vector` – editable vector of numeric components.
* `List` – display a selectable list.
* `Path` – choose files or directories with a dialog.
* `Progress` – read only progress indicator.
* `Action` – button that triggers a method.
* `Title` – show a section title or label.

The following sections give a short overview of the available annotations and
how they can be configured. Unless stated otherwise every annotation accepts a
`readonly=True` flag.

### Number

Use `ui.Number` to display a numeric entry field. Optional `limit_min` and
`limit_max` restrict the range and `precision` controls the number of decimal
places. The implementation automatically selects integer or floating point mode
based on the initial value.

```python
self.count = DataField(0) | ui.Number("Count", limit_min=0, limit_max=10)
```

<!-- add screenshot of Number widget here -->

### Slider

`ui.Slider` creates a slider widget. The range can be defined with
`limit_min` and `limit_max` and a `step_size` may be specified. By default
`show_number_field=True` adds an entry box next to the slider. Set it to
`False` if only the slider should be visible.

```python
self.opacity = DataField(1.0) | ui.Slider("Opacity", limit_min=0, limit_max=1)
```

<!-- add screenshot of Slider widget here -->

### Boolean

`ui.Boolean` shows a check box or switch for boolean values.

```python
self.enabled = DataField(True) | ui.Boolean("Enabled")
```

<!-- add screenshot of Boolean widget here -->

### Text

Use `ui.Text` for single line text entry. A placeholder text can be
configured and the widget can copy its content with `copy_content=True`.

```python
self.message = DataField("Hello") | ui.Text("Message", placeholder_text="enter text")
```

<!-- add screenshot of Text widget here -->

### Options

`ui.Options` displays a drop down list populated with custom values. The list
of choices is passed as a sequence.

```python
self.mode = DataField("auto") | ui.Options("Mode", ["auto", "manual"])
```

<!-- add screenshot of Options widget here -->

### Enum

`ui.Enum` works similar to `Options` but automatically derives the
choices from an enum type.

```python
class Color(Enum):
    Red = 0
    Green = 1
    Blue = 2

self.color = DataField(Color.Red) | ui.Enum("Color")
```

<!-- add screenshot of Enum widget here -->

### Vector

`ui.Vector` allows editing of a fixed length vector of numeric components.
It accepts `vector.obj(x=1, y=2, z=3, t=0)` objects in 2D, 3D or 4D form.
Use `decimal_precision` to control formatting and `labels` to name the
components.

```python
self.position = DataField((0.0, 0.0, 0.0)) | ui.Vector("Position")
```

<!-- add screenshot of Vector widget here -->

### List

`ui.List` shows a selectable list of items. It works together with
`DataList` or `SelectableDataList` models so that changes in the list are
reflected automatically.

```python
from duit.model.DataList import DataList
self.items = DataList() | ui.List("Items")
```

<!-- add screenshot of List widget here -->

### Path

Use `ui.Path` to choose files or directories with a dialog. The annotation
supports three dialog types: `DialogType.OpenFile`, `DialogType.OpenDirectory`
and `DialogType.SaveFile`. The value should be a `Path` object from
`pathlib`. File filters are defined as a mapping of file extensions to
descriptions, for example `{".json": "JSON"}`.

```python
from pathlib import Path
self.output_file = DataField(Path()) | ui.Path(
    "Output",
    dialog_type=ui.PathAnnotation.DialogType.SaveFile,
    filters={".json": "JSON"}
)
```

<!-- add screenshot of Path widget here -->

### Progress

`ui.Progress` displays a read only progress bar. The value is expected to
be a float between 0 and 1.

```python
self.loading = DataField(0.0) | ui.Progress("Loading")
```

<!-- add screenshot of Progress widget here -->

### Action

`ui.Action` shows a button that triggers a callable. By default the
callable runs in a separate thread so the UI does not block. Set
`threaded=False` to execute it on the main thread.

```python
self._on_hello = DataField(self.say_hello) | ui.Action("Press Me")
```

<!-- add screenshot of Action widget here -->

### Title

`ui.Title` inserts a static label or title into the panel and can also
bind to a data field for dynamic text.

```python
self.title = DataField("Hello world") | ui.Title(text_color=(15, 115, 97))
```

<!-- add screenshot of Title widget here -->

### Container Annotations

Container annotations are used to structure a panel into sections. The
`ContainerHelper` simplifies the definition of nested sections using
`StartSection`, `SubSection` and `EndSection` annotations.

```python
from duit import ui
from duit.ui.ContainerHelper import ContainerHelper

class Config:
    def __init__(self):
        helper = ContainerHelper(self)
        with helper.section("User"):
            self.name = DataField("Cat") | ui.Text("Name")
            self.age = DataField(21) | ui.Slider("Age", limit_min=18, limit_max=99)
```

A property panel automatically scans the data context, creates widgets for all
annotated fields and keeps them in sync with the underlying model.
