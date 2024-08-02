class Point:
    EPSILON = 10**-12

    def __init__(self, x, y, type=None, id=None):
        self.x = x
        self.y = y
        self.type = type
        self.id = id

    def __repr__(self):
        return f"{self.id}{self.type if self.type is not None else ''}. ({self.x}, {self.y})"

    def distance(self, other):
        return ((other.x - self.x) ** 2 + (other.y - self.y) ** 2) ** 0.5

    def as_tuple(self):
        return (self.x, self.y)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Point):
            return NotImplemented
        return self.distance(other) < self.EPSILON
    
    def __gt__(self, other: object) -> bool:
        if not isinstance(other, Point):
            return NotImplemented
        if abs(self.x - other.x) < self.EPSILON:
            return self.y > other.y
        return self.x > other.x
    
p1 = Point(2,2)
p2 = Point(2,3)

print(p2 > p1)