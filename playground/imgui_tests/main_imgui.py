import threading
import time
from typing import Callable, Any

import pygfx as gfx
from wgpu.gui.auto import WgpuCanvas, run
from wgpu.utils.imgui import ImguiRenderer

from duit.ui.imgui.ImGuiPropertyPanel import ImGuiPropertyPanel
from duit.ui.imgui.ImGuiPropertyRegistry import init_imgui_registry
from playground.Config import Config


def setup_gui(draw_gui_method: Callable[[], Any]):
    scene = gfx.Scene()

    canvas = WgpuCanvas(size=(1280, 720), max_fps=-1, title="Test", vsync=False)

    renderer = gfx.WgpuRenderer(canvas)
    camera = gfx.PerspectiveCamera(45, 1280 / 720, depth_range=(0.1, 1000))

    direct_light = gfx.DirectionalLight()
    direct_light.local.position = (0, 1, 1)

    scene.add(gfx.AmbientLight(), direct_light)
    scene.add(gfx.AxesHelper())
    camera.show_object(scene)

    gfx.OrbitController(camera, register_events=renderer)

    stats = gfx.Stats(viewport=renderer)

    gui_renderer = ImguiRenderer(renderer.device, canvas)
    gui_renderer.set_gui(draw_gui_method)

    def animate():
        with stats:
            renderer.render(scene, camera, flush=False)
        stats.render()
        gui_renderer.render()
        canvas.request_draw()

    renderer.request_draw(animate)
    run()


def main():
    init_imgui_registry()

    config = Config()
    config.name1.on_changed += lambda v: print(v)

    panel = ImGuiPropertyPanel(lambda: (1280, 720))
    panel.data_context = config

    def on_hungry(value):
        print(f"Hungry changed to: {value}")

    def on_resolution_changed(value):
        print(f"Resolution: {value}")

    config.hungry.on_changed.append(on_hungry)
    config.resolution.on_changed.append(on_resolution_changed)

    def update_loop():
        while True:
            time.sleep(0.1)
            config.age.value += 1

    threading.Thread(target=update_loop, daemon=True).start()

    setup_gui(panel.draw)


if __name__ == '__main__':
    main()
