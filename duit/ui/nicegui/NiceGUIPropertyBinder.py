import asyncio
import threading
import weakref
from typing import Callable, Generic, Optional, TypeVar, Any

from nicegui import ui
from nicegui.element import Element

from duit.model.DataField import DataField

T = TypeVar("T")


class NiceGUIPropertyBinder(Generic[T]):
    """
    Safe two way binding between a NiceGUI element and a DataField.
    Uses DataField.on_changed.append/remove by default.
    Uses element.value by default.
    Provides casting callbacks for UI->model and model->UI.
    """

    def __init__(
            self,
            element: Element,
            model: DataField[T],
            register_ui_change: Optional[Callable[[Callable[[Any], None]], None]],
            to_model: Optional[Callable[[Any], T]] = None,  # cast UI value to model type
            to_ui: Optional[Callable[[T], Any]] = None,  # cast model value to element type
            initial_push_from_model: bool = True,
    ) -> None:
        self._elem_ref = weakref.ref(element)
        self._model = model
        self._loop = asyncio.get_running_loop()
        self._client = ui.context.client
        self._dead = False

        # casting
        self._to_model = to_model or (lambda v: v)
        self._to_ui = to_ui or (lambda v: v)

        # echo suppression
        self._lock = threading.RLock()
        self._ui_to_model_active = False
        self._model_to_ui_active = False

        # UI -> Model
        def ui_changed_wrapper(raw_value: Any) -> None:
            e = self._elem_ref()
            if not e or self._dead:
                return
            with self._lock:
                if self._model_to_ui_active:
                    return
                self._ui_to_model_active = True
            try:
                try:
                    value = self._to_model(raw_value)
                except Exception:
                    return
                self._on_ui_changed(value)
            finally:
                with self._lock:
                    self._ui_to_model_active = False

        register_ui_change(ui_changed_wrapper)

        # Model -> UI
        def model_changed_wrapper(value: T) -> None:
            if self._dead:
                return
            with self._lock:
                if self._ui_to_model_active:
                    return

            def apply() -> None:
                e2 = self._elem_ref()
                if not e2 or self._dead:
                    return
                ui_value = value
                try:
                    ui_value = self._to_ui(value)
                except Exception:
                    return
                with self._lock:
                    self._model_to_ui_active = True
                try:
                    setattr(e2, "value", ui_value)
                except RuntimeError:
                    pass
                except Exception:
                    pass
                finally:
                    with self._lock:
                        self._model_to_ui_active = False

            try:
                self._loop.call_soon_threadsafe(apply)
            except RuntimeError:
                pass

        self._model_cb = model_changed_wrapper
        self._model.on_changed.append(self._model_cb)

        # cleanup on disconnect
        def cleanup(_=None) -> None:
            self.dispose()

        self._client.on_disconnect(cleanup)

        if initial_push_from_model:
            try:
                model_changed_wrapper(self._model.value)
            except Exception:
                pass

    def _on_ui_changed(self, value: T) -> None:
        try:
            self._model.value = value
        except Exception:
            pass

    def dispose(self) -> None:
        if self._dead:
            return
        self._dead = True
        try:
            self._model.on_changed.remove(self._model_cb)
        except Exception:
            pass
