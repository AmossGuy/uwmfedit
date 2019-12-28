import wx

class EditViewport(wx.Window):
    def __init__(self, parent, map_):
        super().__init__(parent, style=wx.FULL_REPAINT_ON_RESIZE)
        
        self.map_ = map_
        
        self.Bind(wx.EVT_PAINT, self.OnPaint)

        #self.Bind(wx.EVT_MIDDLE_DOWN, self.OnMouseDown)
        #self.Bind(wx.EVT_MIDDLE_UP, self.OnMouseUp)
        #self.Bind(wx.EVT_MOTION, self.OnMouseMotion)

    def OnPaint(self, event):
        dc = wx.BufferedPaintDC(self)

        dc.SetBrush(wx.Brush("#2a3439"))
        dc.DrawRectangle(-1, -1, self.GetClientSize()[0] + 2, self.GetClientSize()[1] + 2)

        bitmap = self.GetGrandParent().image.ConvertToBitmap()

        for x in range(self.map_.width):
            for y in range(self.map_.height):
                if self.map_.data[x + y*self.map_.width] != -1:
                    dc.DrawBitmap(bitmap, x*64, y*64, True)
    
    def changemap(self, map_):
        self.map_ = map_
