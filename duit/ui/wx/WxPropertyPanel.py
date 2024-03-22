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


class PanelMixin(wx.Panel, BasePropertyPanel, ABC, metaclass=PanelMeta):
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        BasePropertyPanel.__init__(self)


class WxPropertyPanel(PanelMixin):
    def __init__(self, parent: wx.Window):
        super().__init__(parent=parent)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)

        self._clean_widgets()

    def _clean_widgets(self):
        for child in self.GetChildren():
            child.Destroy()

    def _create_panel(self):
        self._clean_widgets()

        current_panel = self

        vbox = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(vbox)

        root_sizer = wx.FlexGridSizer(rows=0, cols=2, vgap=5, hgap=5)
        current_sizer = root_sizer
        current_sizer.SetFlexibleDirection(wx.HORIZONTAL)
        current_sizer.AddGrowableCol(1, 1)

        vbox.Add(current_sizer)

        annotations = find_all_ui_annotations(self.data_context)

        for var_name, (model, anns) in annotations.items():
            anns = sorted(anns)

            for ann in anns:
                ann_type = type(ann)

                if False and isinstance(ann, StartSectionAnnotation):
                    collapsible_pane = wx.CollapsiblePane(parent=self, label=ann.name, style=wx.CP_DEFAULT_STYLE)

                    current_sizer = wx.FlexGridSizer(rows=0, cols=2, vgap=5, hgap=5)
                    current_sizer.SetFlexibleDirection(wx.HORIZONTAL)
                    current_sizer.AddGrowableCol(1, 1)

                    collapsible_pane.SetSizer(current_sizer)

                    vbox.Add(collapsible_pane)
                    current_panel = collapsible_pane
                    continue

                if False and isinstance(ann, EndSectionAnnotation):
                    if isinstance(current_panel, wx.CollapsiblePane):
                        current_panel = self
                        current_sizer = root_sizer
                    continue

                if ann_type not in UI_PROPERTY_REGISTRY:
                    logging.warning(f"Annotation not registered: {ann_type.__name__}")
                    continue

                property_field = UI_PROPERTY_REGISTRY[ann_type](ann, model)
                widgets = property_field.create_widgets(current_panel)

                for widget in widgets:
                    current_sizer.Add(widget, 0, wx.EXPAND | wx.ALL, border=5)
                    current_panel.Layout()

                current_sizer.Layout()

        current_panel.Layout()
