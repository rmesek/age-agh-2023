from sortedcontainers import SortedList, SortedSet


class Point:
    EPSILON = 10**-12

    def __init__(self, x, y, type, lines=None):
        self.x = x
        self.y = y

        # -1 - początek odcinka
        # 0 - przecięcie odcinków
        # 1 - koniec odcinka
        self.type = type
        if lines is None:
            self.lines = set()
        else:
            self.lines = lines

    def __repr__(self):
        return f"Point({self.x}, {self.y}, {self.type})"

    def distance(self, other):
        return ((other.x - self.x) ** 2 + (other.y - self.y) ** 2) ** 0.5

    def as_tuple(self):
        return (self.x, self.y)

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.type))

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


class Line:
    brush_x = None

    def __init__(self, l_point: Point, r_point: Point, id):
        self.l_point = l_point
        self.r_point = r_point
        self.id = id

    def __repr__(self):
        return f"Line{self.id}({self.l_point}, {self.r_point})"

    def __hash__(self) -> int:
        return hash((self.l_point, self.r_point))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Line):
            return NotImplemented
        return self.id == other.id
        # return self.l_point == other.l_point and self.r_point == other.r_point

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, Line):
            return NotImplemented
        return self.get_y(self.brush_x) > other.get_y(other.brush_x)

    def get_y(self, x: float):
        a = (self.r_point.y - self.l_point.y) / (self.r_point.x - self.l_point.x)
        b = self.r_point.y - a * self.r_point.x
        return a * x + b

    def as_tuple(self):
        return ((self.l_point.x, self.l_point.y), (self.r_point.x, self.r_point.y))


def create_lines(sections: list[tuple[tuple[float, float], tuple[float, float]]]):
    lines = []
    for i, (l_point, r_point) in enumerate(sections):
        if l_point[0] > r_point[0]:
            l_point, r_point = r_point, l_point
        line = Line(Point(l_point[0], l_point[1], -1), Point(r_point[0], r_point[1], 1), i)
        line.l_point.lines.add(line)
        line.r_point.lines.add(line)
        lines.append(line)
    return lines


def det(a: Point, b: Point, c: Point):
    return (a.x - c.x) * (b.y - c.y) - (a.y - c.y) * (b.x - c.x)


def orientation(a: Point, b: Point, c: Point, epsilon=Point.EPSILON):
    d = det(a, b, c)

    # -1 - po lewej stronie prostej
    # 0 - na prostej
    # 1 - po prawej stronie prostej

    if d > epsilon:
        return 1
    elif d < -epsilon:
        return -1
    else:
        return 0


def lines_intersection(line1: Line, line2: Line):
    orientation11 = orientation(line1.l_point, line1.r_point, line2.l_point)
    orientation12 = orientation(line1.l_point, line1.r_point, line2.r_point)
    orientation21 = orientation(line2.l_point, line2.r_point, line1.l_point)
    orientation22 = orientation(line2.l_point, line2.r_point, line1.r_point)

    if orientation11 != orientation12 and orientation21 != orientation22:
        a_1 = (line1.r_point.y - line1.l_point.y) / (line1.r_point.x - line1.l_point.x)
        b_1 = line1.l_point.y - a_1 * line1.l_point.x

        a_2 = (line2.r_point.y - line2.l_point.y) / (line2.r_point.x - line2.l_point.x)
        b_2 = line2.l_point.y - a_2 * line2.l_point.x

        x = (b_2 - b_1) / (a_1 - a_2)
        y = a_1 * (b_2 - b_1) / (a_1 - a_2) + b_1

        return Point(x, y, 0, lines=set([line1, line2]))
    return None


def find_intersections(sections):
    result = []
    lines = create_lines(sections)

    T = SortedList()  # strukturę stanu T
    Q = SortedSet()  # struktura zdarzeń Q
    Line.brush_x = None
    for line in lines:
        Q.add(line.l_point)
        Q.add(line.r_point)

    while Q:
        p = Q.pop(0)
        # Line.brush_x = p.x
        left_neighbour_index = None  # porównaj z następnym odcinkiem
        right_neighbour_index = None  # porónaj z poprzednim odcinkiem

        # zaktualizuj T
        if p.type == -1:  # dodaj odcinek do T
            line = p.lines.pop()
            Line.brush_x = p.x
            T.add(line)
            right_neighbour_index = T.bisect_right(line)
            left_neighbour_index = right_neighbour_index - 2

        elif p.type == 1:  # usuń odcinek z T
            line = p.lines.pop()
            T.remove(line)
            right_neighbour_index = T.bisect_right(line)
            left_neighbour_index = right_neighbour_index - 1

        elif p.type == 0:  # zmień porządek s i s’ w T
            line1 = p.lines.pop()
            line2 = p.lines.pop()
            Line.brush_x -= Point.EPSILON
            T.remove(line1)
            T.remove(line2)
            Line.brush_x += 2 * Point.EPSILON
            T.add(line1)
            T.add(line2)
            right_neighbour_index = max(T.bisect_right(line1), T.bisect_right(line2))
            left_neighbour_index = right_neighbour_index - 3

        # zaktualizuj Q
        new_intersections = set()
        if left_neighbour_index >= 0 and left_neighbour_index + 1 < len(T):
            new_intersections.add(lines_intersection(T[left_neighbour_index], T[left_neighbour_index + 1]))
        if right_neighbour_index - 1 >= 0 and right_neighbour_index < len(T):
            new_intersections.add(lines_intersection(T[right_neighbour_index - 1], T[right_neighbour_index]))
        new_intersections.discard(None)
        for new_intersection in new_intersections:
            if new_intersection not in Q and new_intersection.x > Line.brush_x:
                Q.add(new_intersection)
                result.append((new_intersection.as_tuple(), list(new_intersection.lines)[0].id + 1, list(new_intersection.lines)[1].id + 1))

    return result


sections = [
    ((8.588709677419354, 3.441558441558442), (5.141129032258064, 3.54978354978355)),
    ((7.278225806451612, 4.9567099567099575), (3.1653225806451615, 5.146103896103897)),
]
result = find_intersections(sections)
print(result)
