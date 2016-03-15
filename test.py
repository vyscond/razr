import razr

# Screen
screen = razr.Screen()

# Actors
square = razr.Square((320, 240), 50, "#3300ff")
triangle = razr.Triangle((320, 180), 50, "#ff0033")

class RollingSquare(razr.Square):

    def __init__(self, x, y, size):
        super(RollingSquare, self).__init__((x, y), size, "#3300ff")
        self.patrol_direction = 1
        self.patrol_rot_degree = 8

    def draw(self):
        self.move(x=self.patrol_direction)
        self.rotate(self.patrol_rot_degree)
        if self.origin[razr.X] > 600:
            self.patrol_direction *= -1
            self.patrol_rot_degree *= -1
        elif self.origin[razr.X] < 10:
            self.patrol_direction *= -1
            self.patrol_rot_degree *= -1
        super(RollingSquare, self).draw()

rolling_square = RollingSquare(11, 400, 50)

# Scenes

class MyScene(razr.Scene):

    def keyboard_callback(self, *args):
        print('MyScene > kb > ', args)
        if args[0] == 'r':
            print('rotating')
            self.actors[0].rotate(15)
        if args[0] == 'q':
            screen.quit()

    def keyboard_special_callback(self, key, x, y):
        print('MyScene > ksb > ', key)
        if key == razr.GLUT_KEY_LEFT:
            if self.keyboard_modifier() == razr.GLUT_ACTIVE_SHIFT:
                self.actors[0].rotate(-5)
            self.actors[0].move(-5,0)
        if key == razr.GLUT_KEY_RIGHT:
            if self.keyboard_modifier() == razr.GLUT_ACTIVE_SHIFT:
                self.actors[0].rotate(5)
            self.actors[0].move(5,0)

        if key == razr.GLUT_KEY_UP:
            self.actors[0].move(0,5)
        if key == razr.GLUT_KEY_DOWN:
            self.actors[0].move(0,-5)


scene = MyScene()
scene.actors.append(square)
scene.actors.append(triangle)
scene.actors.append(rolling_square)
# scene1.actors.append(rectangle)

screen.scenes.append(scene)
screen.set_default_scene(0)
screen.run()
