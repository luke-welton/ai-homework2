# Implementation of Hierarchical Clustering
from math import sqrt


class Point:
    def __init__(self, x, y):
        self.coordinates = (x, y)
        self.links = []
        self.label = -1
        self.link_check = False

    def __eq__(self, other):
        try:
            return self.coordinates[0] == other.coordinates[0] and self.coordinates[1] == other.coordinates[1]
        except AttributeError:
            return False

    def find_distance(self, point):
        return sqrt((self.coordinates[0] - point.coordinates[0]) ** 2
                    + (self.coordinates[1] - point.coordinates[1]) ** 2)

    def add_link(self, point):
        self.links.append(point)
        point.links.append(self)

    def label_point(self, value):
        self.label = value
        for link in self.links:
            if link.label < 0:
                link.label_point(value)

    def is_linked(self, point):
        self.link_check = True
        for link in self.links:
            if link == point:
                return True
            elif not link.link_check:
                return link.is_linked(point)


def read_file():
    points = []

    file = open("q6_values.txt", "r")
    if file.mode == "r":
        for line in file.readlines():
            coordinates = line.split()
            points.append(Point(float(coordinates[0]), float(coordinates[1])))

        file.close()
    else:
        file.close()
        print("An error occurred while reading from q6_values.txt\nShutting Down")
        exit(0)

    return points


def find_shortest(points):
    shortest = 0
    point1 = None
    point2 = None

    for i in range(len(points)):
        for j in range(i):
            point = points[i]
            other = points[j]

            if point != other and other not in point.links:
                distance = point.find_distance(other)

                if distance < shortest or shortest == 0:
                    shortest = distance
                    point1 = point
                    point2 = other

    return point1, point2


def output_data(points):
    file = open("q6_output.csv", "w")
    if file.mode == "w":
        file.write("X-Coordinate,Y-Coordinate,Cluster\n")
        for point in points:
            file.write("{},{},{}\n".format(point.coordinates[0], point.coordinates[1], chr(65 + point.label)))

        file.close()
        print("Results output to q6_output.csv")
    else:
        file.close()
        print("An error occurred while writing to q6_output.csv\nShutting Down")
        exit()


def main():
    points = read_file()

    num_clusters = len(points)
    while num_clusters > 2:
        shortest_pair = find_shortest(points)

        if not shortest_pair[0].is_linked(shortest_pair[1]):
            num_clusters -= 1
        for point in points:
            point.link_check = False

        shortest_pair[0].add_link(shortest_pair[1])


    val = 0
    for point in points:
        if point.label < 0:
            point.label_point(val)
            val += 1

    output_data(points)


if __name__ == "__main__":
    main()
