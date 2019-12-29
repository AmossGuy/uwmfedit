import wx

class EditViewport(wx.Window):
    def __init__(self, parent, map_):
        super().__init__(parent, style=wx.FULL_REPAINT_ON_RESIZE)
        
        self.map_ = map_

        self.cameracenter = [0, 0]
        
        self.Bind(wx.EVT_PAINT, self.OnPaint)

        self.Bind(wx.EVT_MIDDLE_DOWN, self.OnMiddleDown)
        self.Bind(wx.EVT_MOTION, self.OnMouseMotion)
        self.Bind(wx.EVT_MIDDLE_UP, self.OnMiddleUp)

    def OnMiddleDown(self, event):
        self.CaptureMouse()
        self.lastmousepos = list(event.GetPosition())

    def OnMouseMotion(self, event):
        if event.MiddleIsDown():
            t = list(event.GetPosition())
            self.cameracenter = list(map(lambda x, y, z: z + (x - y), self.cameracenter, t, self.lastmousepos))
            self.lastmousepos = t
            self.Refresh(False)
        else:
            event.Skip()

    def OnMiddleUp(self, event):
        self.ReleaseMouse()

    def OnPaint(self, event):
        dc = wx.BufferedPaintDC(self)

        dc.SetBrush(wx.Brush("#2a3439"))
        dc.DrawRectangle(-1, -1, self.GetClientSize()[0] + 2, self.GetClientSize()[1] + 2)

        bitmap = self.GetGrandParent().image.ConvertToBitmap()

        for x in range(self.map_.width):
            for y in range(self.map_.height):
                if self.map_.data[x + y*self.map_.width] != -1:
                    coord = self.worldtoscreen((x*64, y*64))
                    dc.DrawBitmap(bitmap, coord[0], coord[1], True)
    
    def changemap(self, map_):
        self.map_ = map_
        self.Refresh(False)

    def worldtoscreen(self, coord):
        return list(map(lambda q, w, e: round(q - w + e/2), coord, self.cameracenter, self.GetClientSize()))
