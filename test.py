import razr

window = razr.Window()

scene1 = razr.Scene(window)

square = razr.Square((320, 240), 50, "#3300ff")
triangle = razr.Triangle((320, 180), 50, "#ff0033")

scene1.actors.append(square)
scene1.actors.append(triangle)

class SpinSquare(razr.Square):
    def __init__(self, *args, **kwargs):
        super(SpinSquare, self).__init__(*args, **kwargs)
        self.rot = 5
    def draw(self):
        self.rotate(self.rot)
        super(SpinSquare, self).draw()

scene1.actors.append(SpinSquare((420, 340), 50, "#33ff00"))

window.run()