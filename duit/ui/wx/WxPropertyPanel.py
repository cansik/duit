import logging
from abc import ABC

import wx

from duit.ui.BasePropertyPanel import BasePropertyPanel
from duit.ui.PropertyRegistry import UI_PROPERTY_REGISTRY
from duit.ui.annotations import find_all_ui_annotations
from duit.ui.annotations.container.EndSectionAnnotation import EndSectionAnnotation
from duit.ui.annotations.container.StartSectionAnnotation import StartSectionAnnotation


class PanelMeta(type(wx.Panel), type(BasePropertyPanel)):
    pass


class PanelMixin(wx.ScrolledWindow, BasePropertyPanel, ABC, metaclass=PanelMeta):
    def __init__(self, *args, **kwargs):
        wx.ScrolledWindow.__init__(self, *args, **kwargs)
        BasePropertyPanel.__init__(self)
        self.SetScrollbars(1, 1, 100, 1000)


class WxPropertyPanel(PanelMixin):
    def __init__(self, parent: wx.Window, vgap: int = 5, hgap: int = 3):
        super().__init__(parent=parent)

        self.vgap = 5
        self.hgap = 5

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)
        self._clean_widgets()

    def _clean_widgets(self):
        for child in self.GetChildren():
            child.Destroy()

    def _create_panel(self):
        self._clean_widgets()

        scrollable_panel = self

        vbox = wx.BoxSizer(wx.VERTICAL)
        scrollable_panel.SetSizer(vbox)

        non_section_sizer = wx.FlexGridSizer(rows=0, cols=2, vgap=self.vgap, hgap=self.hgap)
        non_section_sizer.SetFlexibleDirection(wx.HORIZONTAL)
        non_section_sizer.AddGrowableCol(1, 1)

        # Initial setup for non-section widgets
        current_panel = scrollable_panel
        current_sizer = non_section_sizer

        annotations = find_all_ui_annotations(self.data_context)

        for var_name, (model, anns) in annotations.items():
            anns = sorted(anns)
            in_section = False

            for ann in anns:
                ann_type = type(ann)

                if isinstance(ann, StartSectionAnnotation):
                    collapsible_pane = wx.CollapsiblePane(scrollable_panel, label=ann.name, style=wx.CP_NO_TLW_RESIZE)

                    collapsible_pane.Collapse(ann.collapsed)
                    collapsible_pane.Bind(wx.EVT_COLLAPSIBLEPANE_CHANGED, self.on_collapsible_resized)
                    pane = collapsible_pane.GetPane()
                    new_sizer = wx.FlexGridSizer(rows=0, cols=2, vgap=self.vgap, hgap=self.hgap)
                    new_sizer.SetFlexibleDirection(wx.HORIZONTAL)
                    new_sizer.AddGrowableCol(1, 1)
                    pane.SetSizer(new_sizer)

                    vbox.Add(collapsible_pane, 0, wx.EXPAND | wx.ALL, 5)

                    current_panel = pane
                    current_sizer = new_sizer
                    in_section = True
                    continue

                if isinstance(ann, EndSectionAnnotation):
                    in_section = False
                    current_panel = scrollable_panel
                    current_sizer = non_section_sizer
                    continue

                if ann_type not in UI_PROPERTY_REGISTRY:
                    logging.warning(f"Annotation not registered: {ann_type.__name__}")
                    continue

                property_field = UI_PROPERTY_REGISTRY[ann_type](ann, model)
                widgets = property_field.create_widgets(current_panel)

                for widget in widgets:
                    current_sizer.Add(widget, 0, wx.EXPAND | wx.ALL, 3)

        if not in_section:
            vbox.Add(non_section_sizer, 1, wx.EXPAND)

        self.FitInside()
        scrollable_panel.Layout()

    def on_collapsible_resized(self, event):
        self.Layout()
