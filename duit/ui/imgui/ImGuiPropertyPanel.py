from typing import Callable, Tuple

from imgui_bundle import imgui

from duit.ui.BasePropertyPanel import BasePropertyPanel


class ImGuiPropertyPanel(BasePropertyPanel):
    def __init__(self, display_size_method: Callable[[], Tuple[int, int]]):
        super().__init__()
        self.display_size_method = display_size_method

    def _create_panel(self):
        # is called when the gui structure changes
        pass

    def draw(self):
        width, height = self.display_size_method()

        imgui.new_frame()
        imgui.set_next_window_size((400, 0), imgui.Cond_.always)
        imgui.set_next_window_pos((width - 400, 0), imgui.Cond_.always)

        imgui.set_next_item_open(True)
        is_expand, _ = imgui.begin(
            "Controls",
            None,
            flags=imgui.WindowFlags_.no_move | imgui.WindowFlags_.no_resize,
        )
        value = 0
        is_expand = imgui.collapsing_header("Test")

        if is_expand:
            imgui.slider_float("hello", value, 0, 1)
        imgui.end()

        imgui.end_frame()
        imgui.render()
        return imgui.get_draw_data()
