import razr

# Screen
screen = razr.Screen()

# Actors
square = razr.Square((320, 240), 50, "#3300ff")
triangle = razr.Triangle((320, 180), 50, "#ff0033")

# Scenes

class SquareScene(razr.Scene):

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


scene1 = SquareScene()
scene1.actors.append(square)
scene1.actors.append(triangle)
scene1.actors.append(rectangle)

screen.scenes.append(scene1)
screen.set_default_scene(0)
screen.run()
