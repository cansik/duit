from open3d.cpu.pybind.visualization import gui

from duit.ui.open3d.widgets.SelectionBox import SelectionBox

app = gui.Application.instance
app.initialize()

window: gui.Window = gui.Application.instance.create_window("Demo Window", 200, 400)
vert = gui.Vert()

box = SelectionBox()
box.add_item("hello")
box.add_item("world")
box.add_item("now")
box.add_item("test")
box.add_item("foo")
box.add_item("bas")

vert.add_child(box)
vert.add_child(gui.Button("Click Me"))

window.add_child(vert)

app.run()
