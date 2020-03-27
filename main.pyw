#!/usr/bin/env python3
import wx
import sys
import traceback

from editviewport import EditViewport
from uwmfmap import UwmfMap
from parser import parse, tokenize

class EditorFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="UWMFedit")

        self.image = wx.Image("test_tile.png")

        panel = wx.Panel(self)

        self.canvas = EditViewport(panel, None)

        sizer = wx.BoxSizer()
        sizer.Add(self.canvas, 1, wx.EXPAND)
        panel.SetSizer(sizer)

        menubar = wx.MenuBar()

        filemenu = wx.Menu()
        filemenu.Append(wx.ID_OPEN)

        menubar.Append(filemenu, wx.GetStockLabel(wx.ID_FILE))

        self.SetMenuBar(menubar)

        self.Bind(wx.EVT_MENU, self.OnMenuOpen, id=wx.ID_OPEN)

    def OnMenuOpen(self, event):
        with wx.FileDialog(self, style=wx.FD_OPEN|wx.FD_FILE_MUST_EXIST) as dialog:
            if dialog.ShowModal() == wx.ID_CANCEL:
                return

            with open(dialog.GetPath(), "r", encoding="ascii") as f: # Use ASCII encoding because I don’t feel like dealing with Unicode yet.
                s = f.read()

        self.canvas.changemap(parse(tokenize(s)))

def exceptionhook(type, value, tb):
    dialog = wx.RichMessageDialog(None, caption="", message="Uncaught exception occurred!", style=wx.DIALOG_NO_PARENT|wx.ICON_ERROR|wx.OK|wx.CENTRE)
    dialog.ShowDetailedText("".join(traceback.format_exception(type, value, tb)))
    dialog.ShowModal()
    dialog.Destroy()

if __name__ == "__main__":
    app = wx.App()
    sys.excepthook = exceptionhook
    frame = EditorFrame()
    frame.Show()
    app.MainLoop()
