from razr import Point

# String presentation

points = [
    (10, 10),
    (10.345, 11.345),
    (0, 0),
    (12.345, 12)
]

print(' - Presentation')
for t in points:
    print(Point(t=t))

print(' - Mult')
p = Point(10, 10)
print(p * 2)
print(p * (2, 4))

print(' - Sums')
print(p + 2)
print(p + (2, 4))

print(' - Cast')
a, b = tuple(p)
