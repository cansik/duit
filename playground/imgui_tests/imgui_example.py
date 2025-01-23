import pygfx as gfx
from imgui_bundle import imgui
from wgpu.gui.auto import WgpuCanvas, run
from wgpu.utils.imgui import ImguiRenderer

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


def draw_imgui():
    imgui.new_frame()
    imgui.set_next_window_size((400, 0), imgui.Cond_.always)
    imgui.set_next_window_pos(
        (gui_renderer.backend.io.display_size.x - 400, 0), imgui.Cond_.always
    )
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


gui_renderer.set_gui(draw_imgui)


def animate():
    with stats:
        renderer.render(scene, camera, flush=False)
    stats.render()
    gui_renderer.render()
    canvas.request_draw()


if __name__ == "__main__":
    renderer.request_draw(animate)
    run()
