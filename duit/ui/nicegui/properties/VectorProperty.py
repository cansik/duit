import sys
import typing
from typing import Dict, Optional

from nicegui import ui
from nicegui.element import Element

from duit.event.Event import Event
from duit.model.DataField import DataField
from duit.ui.BaseProperty import M
from duit.ui.annotations import UIAnnotation
from duit.ui.annotations.VectorAnnotation import VectorAnnotation
from duit.ui.nicegui.NiceGUIFieldProperty import NiceGUIFieldProperty
from duit.ui.nicegui.NiceGUIPropertyBinder import NiceGUIPropertyBinder
from duit.ui.nicegui.components.InputNumberField import InputNumberField
from duit.utils import _vector


class VectorProperty(NiceGUIFieldProperty[VectorAnnotation, DataField]):
    """
    A UI component for editing vector properties using one number field per component.
    """

    class _ComponentModel:
        """
        Minimal adapter that exposes a single component of a vector DataField
        as a DataField like object with value and on_changed.
        """

        def __init__(self, parent: DataField, attr_name: str):
            self._parent = parent
            self._name = attr_name
            self.on_changed = Event()

            # forward parent changes as component value changes
            def _parent_changed(_value):
                try:
                    self.on_changed(getattr(self._parent.value, self._name))
                except Exception:
                    pass

            self._parent_cb = _parent_changed
            self._parent.on_changed.append(self._parent_cb)

        @property
        def value(self):
            return getattr(self._parent.value, self._name)

        @value.setter
        def value(self, v):
            setattr(self._parent.value, self._name, v)
            # fire parent after component mutation
            self._parent.fire()

        def dispose(self):
            try:
                self._parent.on_changed.remove(self._parent_cb)
            except Exception:
                pass

    def __init__(self, annotation: UIAnnotation, model: Optional[M] = None, hide_label: bool = False):
        super().__init__(annotation, model, hide_label)
        self._number_fields: Optional[Dict[str, InputNumberField]] = None
        self._component_models: Optional[Dict[str, VectorProperty._ComponentModel]] = None
        self._binders: Optional[Dict[str, NiceGUIPropertyBinder]] = None

    def create_field(self) -> Element:
        ann = self.annotation
        attrs = _vector.get_vector_attributes(self.model.value)
        labels = list(ann.labels) if ann.labels is not None else attrs

        number_fields: Dict[str, InputNumberField] = {}
        self._component_models: Dict[str, VectorProperty._ComponentModel] = {}
        self._binders: Dict[str, NiceGUIPropertyBinder] = {}

        row = ui.row(wrap=False).classes("gap-2 items-center")
        with row:
            for name, label_text in zip(attrs, labels):
                if not ann.hide_labels:
                    ui.label(f"{label_text}:")

                field = (
                    InputNumberField(
                        number_value=getattr(self.model.value, name),
                        min_value=-sys.maxsize - 1,
                        max_value=sys.maxsize,
                        precision=ann.decimal_precision,
                    )
                    .props(self._default_props)
                    .classes("grow")
                )

                if ann.hide_labels:
                    field.tooltip(label_text)
                if ann.tooltip:
                    field.tooltip(ann.tooltip)
                if ann.read_only:
                    field.props("readonly")

                # per component adapter model
                comp_model = VectorProperty._ComponentModel(self.model, name)

                # binder per field
                def register_ui_change(cb, _field=field):
                    _field.on_number_changed += cb

                binder = NiceGUIPropertyBinder(
                    element=field,
                    model=typing.cast(DataField, comp_model),
                    register_ui_change=register_ui_change,
                    to_model=None,
                    to_ui=None,
                    on_dispose=comp_model.dispose
                )

                number_fields[name] = field
                self._component_models[name] = comp_model
                self._binders[name] = binder

        self._number_fields = number_fields
        return row
