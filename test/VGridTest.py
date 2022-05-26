import open3d.visualization.gui as gui
import open3d as o3d


class DemoWindow:
    def __init__(self):
        self.window: gui.Window = gui.Application.instance.create_window("Demo Window", 400, 600)
        self.window.set_on_layout(self._on_layout)
        self.window.set_on_close(self._on_close)

        self.panel = gui.VGrid(2, 15)

        # create key value element
        self.panel.add_child(gui.Label("Name"))
        self.panel.add_child(gui.TextEdit())

        # add multiline key value element
        self.panel.add_child(gui.Label("Vector"))

        vector_panel = gui.Vert()
        vector_panel.add_child(gui.Label("x"))
        vector_panel.add_child(gui.NumberEdit(gui.NumberEdit.DOUBLE))

        vector_panel.add_child(gui.Label("y"))
        vector_panel.add_child(gui.NumberEdit(gui.NumberEdit.DOUBLE))

        self.panel.add_child(vector_panel)

        # add another key value element
        self.panel.add_child(gui.Label("Radius"))
        self.panel.add_child(gui.NumberEdit(gui.NumberEdit.DOUBLE))

        self.window.add_child(self.panel)

    def _on_layout(self, layout_context):
        contentRect = self.window.content_rect
        self.panel.frame = contentRect

    def _on_close(self):
        gui.Application.instance.quit()


if __name__ == "__main__":
    app = o3d.visualization.gui.Application.instance
    app.initialize()

    win = DemoWindow()

    app.run()
