# Implementation of Hierarchical Clustering
from math import sqrt


class Point:
    def __init__(self, x, y):
        self.coordinates = (x, y)
        self.links = []
        self.cluster = None

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


class Cluster:
    def __init__(self, init_point):
        self.points = []
        self.points.append(init_point)
        self.label = ''

        init_point.cluster = self

    def merge(self, other):
        for point in other.points:
            self.points.append(point)
            point.cluster = self


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
            file.write("{},{},{}\n".format(point.coordinates[0], point.coordinates[1], point.cluster.label))

        file.close()
        print("Results output to q6_output.csv")
    else:
        file.close()
        print("An error occurred while writing to q6_output.csv\nShutting Down")
        exit()


def main():
    points = read_file()
    clusters = []

    for point in points:
        clusters.append(Cluster(point))

    while len(clusters) > 2:
        shortest_pair = find_shortest(points)
        shortest_pair[0].add_link(shortest_pair[1])

        if shortest_pair[0].cluster != shortest_pair[1].cluster:
            index = -1
            for i in range(len(clusters)):
                if clusters[i] == shortest_pair[1].cluster:
                    index = i
                    break

            shortest_pair[0].cluster.merge(shortest_pair[1].cluster)
            del clusters[index]

    for i in range(len(clusters)):
        clusters[i].label = chr(65 + i)

    output_data(points)


if __name__ == "__main__":
    main()
