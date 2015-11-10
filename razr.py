from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from colour import Color
import math

class Screen:

    def __init__(self, title='razr engine - OpenGL', width=640, height=480):
        self.title = title
        self.width = width
        self.height = height
        self.scenes = []
        self.scene = None

    def set_default_scene(self, index):
        self.scene = self.scenes[index]

    def show(self):
        self.run()

    def run(self):  # initialization
        # initialize glut
        glutInit()
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
        # set window size
        glutInitWindowSize(self.width, self.height)
        # glutFullScreen()
        # set window position
        glutInitWindowPosition(0, 0)
        # create window with title
        self.window = glutCreateWindow(self.title)
        # set draw function callback
        glutDisplayFunc(self.draw)
        # draw all the time
        glutIdleFunc(self.draw)
        # Keyboard Callbacks
        glutKeyboardFunc(self.keyboard_callback)
        glutSpecialFunc(self.keyboard_special_callback)
        # start everything
        glutMainLoop()

    def keyboard_callback(self, code, x, y):
        if self.scene:
            self.scene.keyboard_callback(code.decode(encoding='ascii'), x, y)

    def keyboard_special_callback(self, code, x, y):
        if self.scene:
            self.scene.keyboard_special_callback(code, x, y)

    def refresh2d(self):
        glViewport(0, 0, self.width, self.height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        # Upper-left origin
        # glOrtho(0.0, self.width, 0.0, self.height, 0.0, 1.0)
        glOrtho(0.0, self.width, self.height, 0.0, 0.0, 1.0)
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

    def __init__(self):
        self.actors = []

    def draw(self):
        for actor in self.actors:
            actor.draw()

    def keyboard_callback(self, key, x, y):
        pass

    def keyboard_special_callback(self, key, x, y):
        pass

class Actor(object):

    def __init__(self):
        self.gravity_factor = 0

    def gravity(self):
        if self.gravity_factor > 0:
            for point in self.matrix:
                point[1] -= self.gravity_factor

    def draw(self):
        raise NotImplementedError('draw not defined')

class Polygon(Actor):

    def __init__(self, origin, radius, vertices):
        super(Polygon, self).__init__()
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

    def move(self, x, y):
        self.origin = (self.origin[0] + x, self.origin[1] + y)
        self.matrix = []
        for vert in range(1,self.vertices+1):
            theta = 2 * math.pi * vert / self.vertices
            x = self.radius * math.cos(theta)
            y = self.radius * math.sin(theta)
            self.matrix.append([x + self.origin[0], y + self.origin[1]])

    def draw(self):
        x, y = 0, 1 # axys
        # checking gravity
        self.gravity()
        glBegin(GL_TRIANGLE_FAN) # filled object
        for point in self.matrix:
            glVertex2f(point[x], point[y])
        glEnd()

    def rotate(self, degree):
        radians = math.radians(-1 * degree)
        cos = math.cos(radians)
        sin = math.sin(radians)
        for point in self.matrix:
            # move the coordinate to the origin
            x, y = point[0] - self.origin[0], point[1] - self.origin[1]
            # make the translation and than move the points to the real origin
            point[0] = ((x * cos) - (y * sin)) + self.origin[0]
            point[1] = ((x * sin) + (y * cos)) + self.origin[1]

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
