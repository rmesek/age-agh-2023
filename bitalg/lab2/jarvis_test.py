class Point:
    def __init__(self, x, y, id=None):
        self.x = x
        self.y = y
        self.id = id  # set to index

    def __repr__(self):
        return f"{self.id}. ({self.x}, {self.y})"

    def as_tuple(self):
        return (self.x, self.y)


def create_points(Q: list[tuple]):
    points = []
    for i, (x, y) in enumerate(Q):
        points.append(Point(x, y, i))
    return points


def to_list_of_tuples(points: list[Point]):
    list_of_tuples = []
    for point in points:
        list_of_tuples.append(point.as_tuple())
    return list_of_tuples


def find_orient(a: Point, b: Point, c: Point):
    """
    Orientacja punktu "c" względem prostej "a b" obliczając wyznacznik macierzy 2x2
    :param a: pierwszey punkt tworzący naszą prostą
    :param b: drugi punkt tworzący naszą prostą
    :param c: punkt, którego położenie względem prostej chcemy znaleźć
    :return: wartość wyznacznika macierzy
            (> 0) => Counterclockwise
            (== 0) => Collinear
            (< 0) => Clockwise
    """
    return (a.x - c.x) * (b.y - c.y) - (a.y - c.y) * (b.x - c.x)


def distance(p1: Point, p2: Point):
    return ((p2.x - p1.x) ** 2 + (p2.y - p1.y) ** 2) ** 0.5


def find_start_point(points: list[Point]):
    return min(points, key=lambda p: (p.x, p.y))


def find_next_point(start_point: Point, points: list[Point], eps=10**-16):
    end_point = points[0]
    for point in points[1:]:
        orient = find_orient(start_point, end_point, point)
        if abs(orient) < eps and distance(start_point, point) > distance(start_point, end_point):
            end_point = point
        elif orient < 0:
            end_point = point
    return end_point


points = [(0,0), (2,0)]
points = create_points(points)
print(find_next_point(Point(0,0), points))
