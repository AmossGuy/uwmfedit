#!/usr/bin/env python3
import wx
from wx import glcanvas
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy

class EditorFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="AmossGuy’s UWMF Editor")

        panel = wx.Panel(self)

        self.canvas = EditCanvas(panel)

        sizer = wx.BoxSizer()
        sizer.Add(self.canvas, 1, wx.EXPAND)
        panel.SetSizer(sizer)

        menubar = wx.MenuBar()
        
        filemenu = wx.Menu()
        filemenu.Append(wx.ID_NEW, "&New\tCtrl+N")
        
        menubar.Append(filemenu, "&File")

        self.SetMenuBar(menubar)

        self.image = wx.Image("test_tile.png")

        #self.Bind(wx.EVT_MENU, self.newfile, id=wx.ID_NEW)

class EditCanvas(glcanvas.GLCanvas):
    def __init__(self, parent):
        super().__init__(parent, style=wx.FULL_REPAINT_ON_RESIZE)

        self.initialized = False
        
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnResize)

    def OnResize(self, event):
        if self.initialized:
            glViewport(0, 0, event.Size.width, event.Size.height)

    def OnPaint(self, event):
        if not self.initialized:
            self.initialize()
        self.draw()

    def initialize(self):
        self.context = glcanvas.GLContext(self)
        self.SetCurrent(self.context)

        rectangle = numpy.array(
            [-0.5,-0.5,  1.0, 0.0, 0.0,
             -0.5, 0.5,  0.0, 1.0, 0.0,
              0.5, 0.5,  0.0, 0.0, 1.0,
              0.5,-0.5,  1.0, 1.0, 1.0],
        dtype=numpy.float32)

        rectangle_elements = numpy.array(
            [0, 1, 2,
             2, 3, 0],
        dtype=numpy.uint8)

        with open("vertex.glsl", "r") as vertex, open("fragment.glsl", "r") as fragment:
            shaders = OpenGL.GL.shaders.compileProgram(
                OpenGL.GL.shaders.compileShader(vertex.read(), GL_VERTEX_SHADER),
                OpenGL.GL.shaders.compileShader(fragment.read(), GL_FRAGMENT_SHADER)
            )

        vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, rectangle.nbytes, rectangle, GL_STATIC_DRAW)

        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 5 * rectangle.itemsize, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 5 * rectangle.itemsize, ctypes.c_void_p(2 * rectangle.itemsize))
        glEnableVertexAttribArray(1)

        elementbuffer = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, elementbuffer)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, rectangle_elements.nbytes, rectangle_elements, GL_STATIC_DRAW)

        glClearColor(0.1, 0.15, 0.1, 1)

        glUseProgram(shaders)
	
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);

        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)

        image = self.GetGrandParent().image
        buffer = image.GetDataBuffer()
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.Width, image.Height, 0, GL_RGB, GL_UNSIGNED_BYTE, numpy.array(buffer, dtype=numpy.uint8))

        self.initialized = True
        
    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT)

        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_BYTE, None)
        
        self.SwapBuffers()

if __name__ == "__main__":
    app = wx.App()
    frame = EditorFrame()
    frame.Show()
    app.MainLoop()
