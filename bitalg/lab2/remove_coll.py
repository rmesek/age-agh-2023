points = [(0, 0), (1, 1), (2, 1), (3, 2)]

for i in reversed(range(1, len(points))):
    p2, p1 = points[i], points[i-1]
    if p1[1] == p2[1]:
        points.pop(i-1)

print(points)