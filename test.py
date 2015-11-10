import razr

# Actors

square = razr.Square((320, 240), 50, "#3300ff")
triangle = razr.Triangle((320, 180), 50, "#ff0033")

#  Scenes

class SquareScene(razr.Scene):

    def keyboard_callback(self, *args):
        print('MyScene > kb > ', args)

    def keyboard_special_callback(self, key, x, y):
        print('MyScene > ksb > ', key)
        if key == razr.GLUT_KEY_LEFT:
            self.actors[0].move(-5,0)
        elif key == razr.GLUT_KEY_RIGHT:
            self.actors[0].move(5,0)

scene1 = SquareScene()
scene1.actors.append(square)

# Screen

screen = razr.Screen()
screen.scenes.append(scene1)
screen.set_default_scene(0)
screen.run()
