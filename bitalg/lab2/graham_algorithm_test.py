def graham_algorithm(Q):
    """
    Funkcja buduje otoczkę wypukłą dla podanego
    zbioru punktów Q algorymem Grahama
    :parm Q: zbiór punktów
    :return: tablica punktów w postaci krotek współrzędnych
    """

    class Point:
        def __init__(self, x, y, id=None):
            self.x = x
            self.y = y
            self.id = id  # set to index

        def __repr__(self):
            return f"{self.id}. ({self.x}, {self.y})"

        def create_points(Q: list[tuple]):
            points = []
            for i, (x, y) in enumerate(Q):
                points.append(Point(x, y, i))
            return points

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
    
    def find_start_point(points: list[Point]):
        return min(points, key=lambda p: (p.y, p.x))

    def sort_points(p0: Point, points: list[Point], eps):
        from functools import cmp_to_key

        def compare(p1: Point, p2: Point, cmp_eps=eps):
            """Will return a negative value for less-than, zero if the inputs are equal, or a positive value for greater-than"""
            orient = find_orient(p0, p1, p2)
            if abs(orient) < eps:
                return 0
            elif orient > 0:
                return -1
            else:
                return 1

        points.sort(key=cmp_to_key(compare))

    def remove_collinear(start_point: Point, points: list[Point]):
        pass


    points = Point.create_points(Q)
    EPS = 10**-16
    start_point = points.pop(find_start_point(points).id)
    sort_points(start_point, points, EPS)
    print(points)

Q = [
        (-62.781083483620016, 9.295526540248986),
        (-10.543100198806997, -26.080520917553812),
        (-81.64932184252287, -74.42163273030921),
        (-36.297317058417946, -72.91194239793609),
        (37.795092197502356, 57.71110085986143),
        (62.511149567563905, -29.172821102708937),
        (21.82806671019955, 2.647377124715007),
        (-46.24539555503924, 42.65521594922478),
        (-77.92302295134137, -7.666110427206263),
        (25.85862324263843, 62.49564419388622),
        (-27.71649622636616, -67.33453457840331),
        (94.83039177581244, -55.52473300629532),
        (-26.29675918891381, -51.30150933048958),
        (-70.11654929355294, 16.723865705806816),
        (26.682887992598097, -65.55763984116587),
        (57.03377667841906, -55.56635171240132),
        (-16.053624841650247, -42.333295668531456),
        (-56.810858686395505, -37.41219002465095),
        (15.604076302407279, -24.85779870929437),
        (-71.77261869976445, -12.306083264402673),
    ]

graham_algorithm(Q)