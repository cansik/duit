import asyncio
import logging
import threading
import weakref
from typing import Callable, Generic, Optional, TypeVar, Any

from nicegui import ui
from nicegui.element import Element

from duit.model.DataField import DataField

T = TypeVar("T")

logger = logging.getLogger(__name__)


class NiceGUIPropertyBinder(Generic[T]):
    """
    Safe two-way binding between a NiceGUI UI element and a DataField model.

    This binder synchronizes values between a UI element and a corresponding model field,
    ensuring consistency when either side changes. It handles UI-to-model and model-to-UI
    conversion, prevents recursive updates, and registers cleanup actions.

    Contract:
    - `register_ui_change` must call the given callback with the raw UI value when the UI changes.
    - `to_model` casts UI value to model value (default: identity function).
    - `to_ui` casts model value to UI-compatible value (default: identity function).
    - `on_dispose` is invoked during cleanup to release resources.

    :param element: The NiceGUI UI element to bind.
    :param model: The DataField representing the data model.
    :param register_ui_change: Function to register a UI change callback.
    :param to_model: Optional function to convert UI value to model value.
    :param to_ui: Optional function to convert model value to UI value.
    :param initial_push_from_model: Whether to push the initial model value to the UI.
    :param on_dispose: Optional cleanup function to call upon disposal.
    """

    def __init__(
            self,
            element: Element,
            model: DataField[T],
            register_ui_change: Callable[[Callable[[Any], None]], None],
            to_model: Optional[Callable[[Any], T]] = None,
            to_ui: Optional[Callable[[T], Any]] = None,
            initial_push_from_model: bool = True,
            on_dispose: Optional[Callable[[], None]] = None,
    ) -> None:
        self._elem_ref = weakref.ref(element)
        self._model = model
        self._loop = asyncio.get_running_loop()
        self._client = ui.context.client
        self._dead = False

        self._to_model = to_model or (lambda v: v)
        self._to_ui = to_ui or (lambda v: v)
        self._on_dispose = on_dispose

        self._lock = threading.RLock()
        self._ui_to_model_active = False
        self._model_to_ui_active = False

        # UI to Model
        def ui_changed_wrapper(raw_value: Any) -> None:
            if self._dead:
                return
            with self._lock:
                if self._model_to_ui_active:
                    return
                self._ui_to_model_active = True
            try:
                value = self._to_model(raw_value)
                self._on_ui_changed(value)
            except Exception as ex:
                logger.warning("NiceGUIPropertyBinder ui-to-model cast or set failed: %s", ex)
            finally:
                with self._lock:
                    self._ui_to_model_active = False

        try:
            register_ui_change(ui_changed_wrapper)
        except Exception as ex:
            logger.warning("NiceGUIPropertyBinder register_ui_change failed: %s", ex)

        # Model to UI
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
                with self._lock:
                    self._model_to_ui_active = True
                try:
                    ui_value = self._to_ui(value)
                    setattr(e2, "value", ui_value)
                except Exception as ex:
                    logger.warning("NiceGUIPropertyBinder model-to-ui cast or set failed: %s", ex)
                finally:
                    with self._lock:
                        self._model_to_ui_active = False

            try:
                self._loop.call_soon_threadsafe(apply)
            except RuntimeError as ex:
                logger.warning("NiceGUIPropertyBinder scheduling failed: %s", ex)

        self._model_cb = model_changed_wrapper
        self._model.on_changed.append(self._model_cb)

        # cleanup on disconnect
        def cleanup(_=None) -> None:
            self.dispose()

        try:
            self._client.on_disconnect(cleanup)
        except Exception as ex:
            logger.warning("NiceGUIPropertyBinder on_disconnect hook failed: %s", ex)

        if initial_push_from_model:
            try:
                model_changed_wrapper(self._model.value)
            except Exception as ex:
                logger.warning("NiceGUIPropertyBinder initial push failed: %s", ex)

    def _on_ui_changed(self, value: T) -> None:
        """
        Internal method called when the UI value changes.

        Updates the model with the converted UI value.

        :param value: The converted value from the UI to update the model with.
        """
        try:
            self._model.value = value
        except Exception as ex:
            logger.warning("NiceGUIPropertyBinder setting model value failed: %s", ex)

    def dispose(self) -> None:
        """
        Disposes of the binder by unsubscribing from model changes and invoking cleanup.

        This should be called to avoid memory leaks when the element is no longer in use.
        """
        if self._dead:
            return
        self._dead = True
        try:
            self._model.on_changed.remove(self._model_cb)
        except Exception as ex:
            logger.warning("NiceGUIPropertyBinder unsubscribe failed: %s", ex)
        try:
            if self._on_dispose is not None:
                self._on_dispose()
        except Exception as ex:
            logger.warning("NiceGUIPropertyBinder on_dispose failed: %s", ex)
