# Implementation of k-means algorithm
from math import sqrt
from copy import deepcopy


class Point:
    def __init__(self, x, y):
        self.coordinates = (x, y)

    def find_cluster(self, clusters):
        closest_distance = 0
        closest_cluster = None
        for cluster in clusters:
            dist = sqrt((self.coordinates[0] - cluster.coordinates[0]) ** 2
                        + (self.coordinates[1] - cluster.coordinates[1]) ** 2)

            if closest_cluster is None or dist < closest_distance:
                closest_distance = dist
                closest_cluster = cluster

        return closest_cluster


class Cluster:
    def __init__(self, x, y):
        self.coordinates = (x, y)
        self.points = []

    def add_point(self, point):
        self.points.append(point)

    def recalculate(self):
        x = 0
        y = 0
        for point in self.points:
            x += point.coordinates[0]
            y += point.coordinates[1]

        x /= len(self.points)
        y /= len(self.points)

        self.coordinates = (x, y)
        self.points = []


class ClusterArray:
    def __init__(self):
        self.i = 0
        self.clusters = []

    def __eq__(self, other):
        try:
            for i in range(len(self.clusters)):
                a = self.clusters[i]
                b = other.clusters[i]

                if a.coordinates[0] != b.coordinates[0] or a.coordinates[1] != b.coordinates[1]:
                    return False
            return True
        except (AttributeError, IndexError):
            return False

    def __iter__(self):
        return (cluster for cluster in self.clusters)

    def add_cluster(self, cluster):
        self.clusters.append(cluster)


def read_file():
    points = []

    file = open("q5_values.txt", "r")
    if file.mode == "r":
        for line in file.readlines():
            coordinates = line.split()
            point = Point(float(coordinates[0]), float(coordinates[1]))
            points.append(point)

        file.close()
    else:
        file.close()

        print("An error occurred while opening q5 values.txt. Shutting Down.")
        exit(0)

    return points


def main():
    clusters = ClusterArray()
    points = read_file()

    for _ in range(3):
        clusters.add_cluster(Cluster(0.0, 0.0))

    old_clusters = None
    new_clusters = clusters
    while old_clusters != new_clusters:
        old_clusters = deepcopy(new_clusters)

        for point in points:
            nearest_cluster = point.find_cluster(new_clusters)
            nearest_cluster.add_point(point)

        for cluster in new_clusters:
            cluster.recalculate()


if __name__ == "__main__":
    main()
