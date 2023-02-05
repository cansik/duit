import open3d
import open3d.visualization.gui as gui

from duit.ui.open3d.Open3dPropertyPanel import Open3dPropertyPanel


class DemoWindow:
    def __init__(self, data_context):
        self.window: gui.Window = gui.Application.instance.create_window("Demo Window", 400, 600)
        self.window.set_on_layout(self._on_layout)
        self.window.set_on_close(self._on_close)

        em = self.window.theme.font_size
        separation_height = int(round(0.5 * em))

        self.panel = Open3dPropertyPanel(em)
        self.window.add_child(self.panel)

        self.panel.data_context = data_context

    def _on_layout(self, layout_context):
        contentRect = self.window.content_rect
        self.panel.frame = contentRect

    def _on_close(self):
        gui.Application.instance.quit()
