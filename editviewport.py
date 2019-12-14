import wx
from wx import glcanvas
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy

class EditViewport(glcanvas.GLCanvas):
    def __init__(self, parent, map):
        super().__init__(parent, style=wx.FULL_REPAINT_ON_RESIZE)

        self.initialized = False
        
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnResize)

        self.Bind(wx.EVT_MIDDLE_DOWN, self.OnMouseDown)
        self.Bind(wx.EVT_MIDDLE_UP, self.OnMouseUp)
        self.Bind(wx.EVT_MOTION, self.OnMouseMotion)

        self.map = map

        self.generatevbo()

    def OnMouseDown(self, event):
        self.CaptureMouse()
        self.oldmx, self.oldmy = self.newmx, self.newmy = event.GetPosition()

    def OnMouseUp(self, event):
        self.ReleaseMouse()

    def OnMouseMotion(self, event):
        if event.MiddleIsDown():
            self.oldmx, self.oldmy = self.newmx, self.newmy
            self.newmx, self.newmy = event.GetPosition()
            self.smx, self.smy = self.smx - (self.newmx - self.oldmx), self.smy - (self.newmy - self.oldmy)
            glUniform2f(glGetUniformLocation(self.shaders, "screenmiddle"), self.smx, self.smy)
            self.Refresh(False)

    def OnResize(self, event):
        if self.initialized:
            glViewport(0, 0, event.Size.width, event.Size.height)
            glUniform2f(glGetUniformLocation(self.shaders, "screensize"), event.Size.width, event.Size.height)

    def OnPaint(self, event):
        if not self.initialized:
            self.initialize()
        self.draw()

    def changemap(self, map):
        self.map = map
        self.generatevbo()
        glBindBuffer(GL_ARRAY_BUFFER, self.vbop)
        glBufferData(GL_ARRAY_BUFFER, self.vbo.nbytes, self.vbo, GL_DYNAMIC_DRAW)
        self.draw()
    
    def initialize(self):
        self.context = glcanvas.GLContext(self)
        self.SetCurrent(self.context)

        rectangle = numpy.array(
            [-32.0,-32.0,  0.0, 0.0,
             -32.0, 32.0,  0.0, 1.0,
              32.0, 32.0,  1.0, 1.0,
              32.0,-32.0,  1.0, 0.0],
        dtype=numpy.float32)

        rectangle_elements = numpy.array(
            [0, 1, 2,
             2, 3, 0],
        dtype=numpy.uint8)

        with open("vertex.glsl", "r") as vertex, open("fragment.glsl", "r") as fragment:
            self.shaders = OpenGL.GL.shaders.compileProgram(
                OpenGL.GL.shaders.compileShader(vertex.read(), GL_VERTEX_SHADER),
                OpenGL.GL.shaders.compileShader(fragment.read(), GL_FRAGMENT_SHADER)
            )

        self.vbop = vbo = glGenBuffers(1)
        #glBindBuffer(GL_ARRAY_BUFFER, vbo)
        #glBufferData(GL_ARRAY_BUFFER, rectangle.nbytes, rectangle, GL_STATIC_DRAW)

        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vbo.nbytes, self.vbo, GL_DYNAMIC_DRAW)

        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 4 * self.vbo.itemsize, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 4 * self.vbo.itemsize, ctypes.c_void_p(2 * self.vbo.itemsize))
        glEnableVertexAttribArray(1)

        elementbuffer = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, elementbuffer)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, rectangle_elements.nbytes, rectangle_elements, GL_STATIC_DRAW)

        glClearColor(0.1, 0.15, 0.1, 1)

        glUseProgram(self.shaders)

        self.texture = glGenTextures(1)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture)

        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

        glUniform1i(glGetUniformLocation(self.shaders, "ourtexture"), 0)
        glUniform2f(glGetUniformLocation(self.shaders, "screensize"), self.GetSize().x, self.GetSize().y)
        glUniform2f(glGetUniformLocation(self.shaders, "screenmiddle"), 0, 0)
        self.smx, self.smy = 0, 0

        image = self.GetGrandParent().image
        buffer = image.GetDataBuffer()
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.Width, image.Height, 0, GL_RGB, GL_UNSIGNED_BYTE, numpy.array(buffer, dtype=numpy.uint8))

        self.initialized = True
        
    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT)

        glDrawArrays(GL_TRIANGLES, 0, len(self.vbo));
        
        self.SwapBuffers()

    def generatevbo(self):
        vbo = []
        for y in range(len(self.map.data)):
            for x in range(len(self.map.data[y])):
                if self.map.data[y][x] != -1:
                    topleft = (x * self.map.tilesize, y * self.map.tilesize, 0, 0)
                    bottomleft = (x * self.map.tilesize, (y+1) * self.map.tilesize, 0, 1)
                    bottomright = ((x+1) * self.map.tilesize, (y+1) * self.map.tilesize, 1, 1)
                    topright = ((x+1) * self.map.tilesize, y * self.map.tilesize, 1, 0)
                    
                    vbo.extend(topleft)
                    vbo.extend(bottomleft)
                    vbo.extend(topright)

                    vbo.extend(topright)
                    vbo.extend(bottomleft)
                    vbo.extend(bottomright)
        self.vbo = numpy.array(vbo, dtype=numpy.float32)
