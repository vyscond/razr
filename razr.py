from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from colour import Color
import math

class Window:

    def __init__(self, title='razr engine - OpenGL', width=640, height=480):
        self.title = title
        self.width = width
        self.height = height
        self.scene = None

    def run(self):  # initialization
        # initialize glut
        glutInit()
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
        # set window size
        glutInitWindowSize(self.width, self.height)
        # set window position
        glutInitWindowPosition(0, 0)
        # create window with title
        self.window = glutCreateWindow(self.title)
        # set draw function callback
        glutDisplayFunc(self.draw)
        # draw all the time
        glutIdleFunc(self.draw)
        # start everything
        glutMainLoop()

    def refresh2d(self):
        glViewport(0, 0, self.width, self.height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0.0, self.width, 0.0, self.height, 0.0, 1.0)
        glMatrixMode (GL_MODELVIEW)
        glLoadIdentity()

    def draw(self):
        # clear the screen
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # reset position
        glLoadIdentity()
        self.refresh2d()
        # ToDo draw rectangle
        if self.scene:
            self.scene.draw()
        # important for double buffering
        glutSwapBuffers()

class Scene:

    def __init__(self, window):
        self.window = window
        self.window.scene = self
        self.actors = []

    def draw(self):
        for actor in self.actors:
            actor.draw()

class Actor(object):

    def draw(self):
        raise NotImplementedError('draw not defined')

class Polygon(Actor):

    def __init__(self, origin, radius, vertices):
        self.origin = origin
        self.radius = radius
        self.vertices = vertices
        self.matrix = []
        for vert in range(1,self.vertices+1):
            theta = 2 * math.pi * vert / self.vertices
            x = radius * math.cos(theta)
            y = radius * math.sin(theta)
            self.matrix.append([x + self.origin[0], y + self.origin[1]])
            # self.matrix.append([x, y])

    def draw(self):
        x, y = 0, 1
        glBegin(GL_TRIANGLE_FAN) # filled object
        for point in self.matrix:
            glVertex2f(point[x], point[y])
        glEnd()

    def rotate(self, degree):
        radians = math.radians(-1 * degree)
        cos = math.cos(radians)
        sin = math.sin(radians)
        for point in self.matrix:
            # tmp_x = cos * (point[0] - self.origin[0]) - sin * (point[1] - self.origin[1]) + self.origin[0]
            # tmp_y = sin * (point[0] - self.origin[0]) + cos * (point[1] - self.origin[1]) + self.origin[1]
            print('({}, {})'.format(tmp_x, tmp_y))
            point[0] = ((cos * (point[0] - self.origin[0])) - (sin * (point[1] - self.origin[1]))) + self.origin[0]
            point[1] = ((sin * (point[0] - self.origin[0])) + (cos * (point[1] - self.origin[1]))) + self.origin[1]

    def show(self):
        for c in self.matrix:
            print(c)

class Triangle(Polygon):

    def __init__(self, origin, size, color="#000000"):
        super(Triangle, self).__init__(origin, size/2, 3)
        self.color = Color(color)

    def draw(self):
        glColor3f(self.color.red, self.color.green, self.color.blue)
        super(Triangle, self).draw()

class Square(Polygon):

    def __init__(self, origin, size, color="#000000"):
        super(Square, self).__init__(origin, size/2, 4)
        self.color = Color(color)

    def draw(self):
        glColor3f(self.color.red, self.color.green, self.color.blue)
        super(Square, self).draw()

# class Rectangle(Polygon):

#     def __init__(self, origin, width, height, color="#000000"):
#         self.origin = origin
#         self.width = width
#         self.height = height

#         matrix = [
#             [x, y],
#             [x + width, y],
#             [x + width, y + height],
#             [x, y + height]
#         ]
#         super(Rectangle, self).__init__(matrix)

#     def draw(self):
#         glColor3f(self.color.red, self.color.green, self.color.blue)
#         glBegin(GL_QUADS)  # start drawing a rectangle
#         super(Rectangle, self).draw()
