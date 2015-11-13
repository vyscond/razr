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

    def quit(self):
        glutDestroyWindow(self.window)
        exit()

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

    def keyboard_modifier(self):
        return glutGetModifiers()

class Actor(object):

    def __init__(self, gforce=0):
        self.gforce = gforce

    def draw(self):
        raise NotImplementedError('draw not defined')

class Polygon(Actor):

    def __init__(self, origin, vertices, radius, degree=45, color="#000000"):
        super(Polygon, self).__init__()
        self.origin = origin
        self.radius = radius
        self.vertices = vertices
        self.matrix = []
        self.radians = math.radians(degree)
        self.color = Color(color)
        print('Polygon > processing {} vertices'.format(self.vertices+1))
        for vert in range(1,self.vertices+1):
            theta = 2 * math.pi * vert / self.vertices
            # there is a specific length for every point
            if type(self.radius) == list:
                r = radius[vert - 1]
            # equal length to every point
            else:
                r = radius
            # plotting the coordinates with a initial degree rotation
            x = r * math.cos(theta - self.radians)
            y = r * math.sin(theta - self.radians)
            self.matrix.append([x + self.origin[0], y + self.origin[1]])
            # self.matrix.append([x, y])

    def apply_gravity(self):
        if self.gforce > 0:
            self.move(0, -(self.gravity_factor))

    def draw(self):
        x, y = 0, 1 # axys
        # coloring
        glColor3f(self.color.red, self.color.green, self.color.blue)
        # checking gravity
        self.apply_gravity()
        # filled object
        glBegin(GL_TRIANGLE_FAN)
        # drawing coordinates
        for point in self.matrix:
            glVertex2f(point[x], point[y])
        glEnd()

    def move(self, x, y):
        self.origin = (self.origin[0] + x, self.origin[1] + y)
        for point in self.matrix:
            print("x={} -> x'={}".format(point[0], point[0]+x))
            point[0] += x
            point[1] += y

    def rotate(self, degree):
        radians = math.radians(-1 * degree)
        cos = math.cos(radians)
        sin = math.sin(radians)
        for point in list(self.matrix):
            # move the coordinate to the origin
            x, y = point[0] - self.origin[0], point[1] - self.origin[1]
            # make the translation and than move the points to the real origin
            point[0] = ((x * cos) - (y * sin)) + self.origin[0]
            point[1] = ((x * sin) + (y * cos)) + self.origin[1]
        # self.radians += radians

    def show(self):
        for c in self.matrix:
            print(c)

class Triangle(Polygon):

    def __init__(self, origin, size, color="#000000"):
        super(Triangle, self).__init__(origin, 3, size/2, degree=30, color=color)

class Square(Polygon):

    def __init__(self, origin, size, color="#000000"):
        super(Square, self).__init__(origin, 4, size/2, color=color)

# class Rectangle(Polygon):
#
#     def __init__(self, origin, width, height, color="#000000"):
#         super(Rectangle, self).__init__(origin, 4, [height/2, width, height/2, width], degree=10, color=color)
