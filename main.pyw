#!/usr/bin/env python3
import wx

from editviewport import EditViewport
from uwmfmap import UwmfMap

class EditorFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="AmossGuy’s UWMF Editor")

        self.image = wx.Image("test_tile.png")

        panel = wx.Panel(self)

        self.canvas = EditViewport(panel, UwmfMap())

        sizer = wx.BoxSizer()
        sizer.Add(self.canvas, 1, wx.EXPAND)
        panel.SetSizer(sizer)

        menubar = wx.MenuBar()
        
        filemenu = wx.Menu()
        filemenu.Append(wx.ID_NEW)
        
        menubar.Append(filemenu, wx.GetStockLabel(wx.ID_FILE))

        self.SetMenuBar(menubar)

        self.Bind(wx.EVT_MENU, self.OnMenuNew, id=wx.ID_NEW)

    def OnMenuNew(self, event):
        self.canvas.changemap(UwmfMap())

if __name__ == "__main__":
    app = wx.App()
    frame = EditorFrame()
    frame.Show()
    app.MainLoop()
