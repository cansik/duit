import logging
from abc import ABC

import wx

from duit.collections.Stack import Stack
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

        vbox.Add(current_sizer, 1, wx.EXPAND)

        annotations = find_all_ui_annotations(self.data_context)

        # Initialize stack for panels and sizers
        panel_sizer_stack = Stack()

        for var_name, (model, anns) in annotations.items():
            anns = sorted(anns)

            for ann in anns:
                ann_type = type(ann)

                if isinstance(ann, StartSectionAnnotation):
                    # Create a new collapsible pane and flex grid sizer
                    collapsible_pane = wx.CollapsiblePane(current_panel, label=ann.name)

                    pane = collapsible_pane.GetPane()
                    new_sizer = wx.FlexGridSizer(rows=0, cols=2, vgap=5, hgap=5)
                    new_sizer.SetFlexibleDirection(wx.HORIZONTAL)
                    new_sizer.AddGrowableCol(1, 1)
                    pane.SetSizer(new_sizer)

                    current_sizer.Add(collapsible_pane, 0, wx.EXPAND | wx.ALL, 5)
                    current_panel.Layout()

                    # Push current context onto stack
                    panel_sizer_stack.push((current_panel, current_sizer))

                    # Set new context
                    current_panel = pane
                    current_sizer = new_sizer
                    continue

                if isinstance(ann, EndSectionAnnotation):
                    if not panel_sizer_stack.is_empty:
                        # Pop the last panel and sizer from the stack
                        current_panel, current_sizer = panel_sizer_stack.pop()
                    continue

                if ann_type not in UI_PROPERTY_REGISTRY:
                    logging.warning(f"Annotation not registered: {ann_type.__name__}")
                    continue

                property_field = UI_PROPERTY_REGISTRY[ann_type](ann, model)
                widgets = property_field.create_widgets(current_panel)

                for widget in widgets:
                    current_sizer.Add(widget, 0, wx.EXPAND | wx.ALL, 5)
                    current_panel.Layout()

                current_sizer.Layout()

        current_panel.Layout()
