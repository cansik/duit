import logging
from abc import ABC
from functools import partial
from typing import Any, Union

import wx

from duit.ui.BasePropertyPanel import BasePropertyPanel
from duit.ui.PropertyRegistry import UI_PROPERTY_REGISTRY
from duit.ui.annotations import find_all_ui_annotations
from duit.ui.annotations.container.EndSectionAnnotation import EndSectionAnnotation
from duit.ui.annotations.container.StartSectionAnnotation import StartSectionAnnotation
from duit.ui.annotations.container.SubSectionAnnotation import SubSectionAnnotation
from duit.ui.wx.widgets.WxCollapsablePanel import WxCollapsiblePane


class PanelMeta(type(wx.Panel), type(BasePropertyPanel)):
    pass


class PanelMixin(wx.ScrolledWindow, BasePropertyPanel, ABC, metaclass=PanelMeta):
    def __init__(self, *args, **kwargs):
        wx.ScrolledWindow.__init__(self, *args, style=wx.VSCROLL | wx.HSCROLL, **kwargs)
        BasePropertyPanel.__init__(self)
        # self.SetScrollbars(1, 1, 100, 1000)
        self.SetScrollRate(5, 5)  # Adjust scroll rate for smoother scrolling
        self.SetExtraStyle(wx.WS_EX_PROCESS_UI_UPDATES | wx.BUFFER_VIRTUAL_AREA)  # Optional double-buffering
        self.SetAutoLayout(True)


class WxPropertyPanel(PanelMixin):
    def __init__(self, parent: wx.Window, vgap: int = 3, hgap: int = 3):
        super().__init__(parent=parent)

        self.vgap = vgap
        self.hgap = hgap

        self.max_stack_depth = 5
        self.stack_depth = 0

    def _clean_widgets(self):
        for child in self.GetChildren():
            if isinstance(child, wx.ScrollBar) or isinstance(child, wx.Window):
                continue
            child.Destroy()

    def _create_panel(self):
        self._clean_widgets()

        if self._data_context is None:
            return

        self._create_properties(self._data_context, self)

        self.Layout()
        self.FitInside()

    def _create_properties(self, obj: Any, panel: Union[wx.Panel, "WxPropertyPanel"]):
        self.stack_depth += 1

        vbox = wx.BoxSizer(wx.VERTICAL)
        panel.SetSizer(vbox)

        non_section_sizer = wx.FlexGridSizer(rows=0, cols=2, vgap=self.vgap, hgap=self.hgap)
        non_section_sizer.SetFlexibleDirection(wx.HORIZONTAL)
        non_section_sizer.AddGrowableCol(1, 1)

        # Initial setup for non-section widgets
        current_panel = panel
        current_sizer = non_section_sizer

        annotations = find_all_ui_annotations(obj)

        in_section = False
        for var_name, (model, anns) in annotations.items():
            anns = sorted(anns)
            in_section = False

            for ann in anns:
                ann_type = type(ann)

                is_sub_section = isinstance(ann, SubSectionAnnotation)
                if isinstance(ann, StartSectionAnnotation) or is_sub_section:
                    if is_sub_section:
                        if self.stack_depth > self.max_stack_depth:
                            logging.info(f"Stack ({self.stack_depth}) depth is at limit {self.max_stack_depth}.")
                            continue

                    # setup pane
                    collapsible_pane = WxCollapsiblePane(panel, label=ann.name, style=wx.CP_NO_TLW_RESIZE)
                    collapsible_pane.Collapse(ann.collapsed)
                    collapsible_pane.Bind(wx.EVT_COLLAPSIBLEPANE_CHANGED, self.on_collapsible_resized)

                    pane = collapsible_pane.GetPane()
                    new_sizer = wx.FlexGridSizer(rows=0, cols=2, vgap=self.vgap, hgap=self.hgap)
                    new_sizer.SetFlexibleDirection(wx.HORIZONTAL)
                    new_sizer.AddGrowableCol(1, 1)
                    pane.SetSizer(new_sizer)

                    vbox.Add(collapsible_pane, 0, wx.EXPAND | wx.ALL, 0)

                    # implementation of active field link
                    if ann.is_active_field is not None:
                        def _show_or_hide(value: bool, w: wx.Control):
                            if value:
                                w.Show()
                            else:
                                w.Hide()
                            w.GetParent().Layout()

                        ann.is_active_field.on_changed += partial(_show_or_hide, w=collapsible_pane)
                        ann.is_active_field.fire_latest()

                    if ann.name_field is not None:
                        def _update_label(value: str, w: WxCollapsiblePane):
                            w.SetLabel(value)

                        ann.name_field.on_changed += partial(_update_label, w=collapsible_pane)
                        ann.name_field.fire_latest()

                    if is_sub_section:
                        # add widgets and continue
                        self._create_properties(model.value, pane)
                        continue

                    current_panel = pane
                    current_sizer = new_sizer
                    in_section = True
                    continue

                if isinstance(ann, EndSectionAnnotation):
                    in_section = False
                    current_panel = panel
                    current_sizer = non_section_sizer
                    continue

                if ann_type not in UI_PROPERTY_REGISTRY:
                    logging.warning(f"Annotation not registered: {ann_type.__name__}")
                    continue

                property_field = UI_PROPERTY_REGISTRY[ann_type](ann, model)
                widgets = property_field.create_widgets(current_panel)

                for widget in widgets:
                    current_sizer.Add(widget, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 0)

        if not in_section:
            vbox.Add(non_section_sizer, 1, wx.EXPAND)

    def on_collapsible_resized(self, event):
        self.Layout()
