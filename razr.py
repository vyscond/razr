import timeit
import math
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from colour import Color

X, Y = 0, 1

class Resolutions:

    VGA    = (640 , 480)
    SVGA   = (800 , 600)
    WSVGA  = (1024, 600)
    XGA    = (1024, 768)
    XGAP   = (1152, 864)
    WXGA   = (1280, 720)
    WXGA   = (1280, 768)
    WXGA   = (1280, 800)
    SXGA   = (1280, 1024)
    HD     = (1360, 768)
    HD6    = (1366, 768)
    WXGAP  = (1440, 900)
    HDP    = (1600, 900)
    UXGA   = (1600, 1200)
    WSXGAP = (1680, 1050)
    FHD    = (1920, 1080)
    WUXGA  = (1920, 1200)
    QHD    = (2560, 1440)
    WQXGA  = (2560, 1600)
    FOURK  = (3840, 2160)

class Utils(object):

    def log(self, msg):
        print('{} - {}'.format(
            self.__class__.__name__,
            msg
        ))

class Screen:

    def __init__(self, title='razr engine - OpenGL', width=640, height=480, resolution=Resolutions.VGA):
        self.title = title
        self.width = width
        self.height = height
        self.scenes = []
        self.scene = None
        self.fps = 30

    def set_default_scene(self, index):
        '''
        Most of the time this will be used to point the "menu" Scene
        '''
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
        '''
        Every Scene already have a callback like this one. No need to register
        it manually
        '''
        if self.scene:
            self.scene.keyboard_callback(code.decode(encoding='ascii'), x, y)

    def keyboard_special_callback(self, code, x, y):
        '''
        Every Scene already have a callback like this one. No need to register
        it manually
        '''
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
        try:
            glutDestroyWindow(self.window)
        except NameError:
            print('looks like we never rendered squat!')
        exit()

class Scene(object):

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

class Actor(Utils):

    def __init__(self, gforce=0):
        self.gforce = gforce

    def draw(self):
        raise NotImplementedError('draw not defined')

class CommonPhysic(object):

    def is_colliding(self, ):
        pass

class Point(object):

    def __init__(self, x=0, y=0, t=None):
        if t:
            self.x, self.y = t
        else:
            self.x = x
            self.y = y

    def __sub__(self, k):
        if type(k) == tuple:
            self.x -= k[X]
            self.y -= k[Y]
        elif type(k) == int:
            self.x -= k
            self.y -= k
        return self

    def __add__(self, k):
        if type(k) == tuple:
            self.x += k[X]
            self.y += k[Y]
        elif type(k) == int:
            self.x += k
            self.y += k
        return self

    def __mul__(self, k):
        if type(k) == tuple:
            self.x *= k[X]
            self.y *= k[Y]
        elif type(k) == int:
            self.x *= k
            self.y *= k
        return self

    def __iter__(self):
        return iter([self.x, self.y])

    def __str__(self):
        return 'point({:0.2f}, {:0.2f})'.format(self.x, self.y)


class Polygon(Actor):
    '''
    Base Helper for geomtric based actor
    '''
    def __init__(self, origin, vertices, radius, degree=45, color="#000000"):
        super(Polygon, self).__init__()
        self.origin = origin
        self.radius = radius
        self.vertices = vertices
        self.matrix = []
        self.radians = math.radians(degree)
        self.color = Color(color)
        self.log('processing {} vertices'.format(self.vertices+1))
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

    def draw(self):
        # coloring
        glColor3f(self.color.red, self.color.green, self.color.blue)

        # filled object
        glBegin(GL_TRIANGLE_FAN)

        # drawing coordinates
        for point in self.matrix:
            glVertex2f(point[X], point[Y])

        glEnd()

    def move(self, x=0, y=0):
        if x != 0 or y != 0:
            self.origin = (self.origin[X] + x, self.origin[Y] + y)
            for point in self.matrix:
                self.log("({:0.2f}, {:0.2f}) -> ({:0.2f}, {:0.2f})'".format(point[X], point[Y], point[X]+x, point[Y]+y))
                point[X] += x
                point[Y] += y

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
