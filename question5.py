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


class ClusterArray:
    def __init__(self):
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

    def empty_clusters(self):
        for cluster in self.clusters:
            cluster.points = []

    def calculate_distortion(self):
        distortion = 0
        for cluster in self.clusters:
            cluster_sum = 0
            for point in cluster.points:
                d = (point.coordinates[0] - cluster.coordinates[0], point.coordinates[1] - cluster.coordinates[1])
                cluster_sum += d[0] ** 2 + d[1] ** 2
            distortion += cluster_sum

        return distortion

    def output_data(self):
        file = open("q5_output.csv", "w")
        if file.mode == "w":
            letter = 'A'
            for cluster in self.clusters:
                for point in cluster.points:
                    file.write(str(point.coordinates[0]) + "," + str(point.coordinates[1]) + "," + letter + "\n")
                letter = chr(ord(letter) + 1)

            file.close()
        else:
            file.close()

            print("An error occurred while writing to q5_output.csv. Shutting Down.")
            exit(0)


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


def calculate_cluster_points(points):
    sort_x = []
    sort_y = []

    for point in points:
        sort_x.append(point.coordinates[0])
        sort_y.append(point.coordinates[1])

    sort_x.sort()
    sort_y.sort()

    mid = round(len(points) / 2)
    quart = round(mid / 2)

    return [
        (sort_x[mid - quart], sort_y[mid - quart]),
        (sort_x[mid], sort_y[mid]),
        (sort_x[mid + quart], sort_y[mid + quart])
    ]


def main():
    clusters = ClusterArray()
    points = read_file()

    for point in calculate_cluster_points(points):
        clusters.add_cluster(Cluster(point[0], point[1]))

    old_clusters = None
    while old_clusters != clusters:
        old_clusters = deepcopy(clusters)
        clusters.empty_clusters()

        for point in points:
            nearest_cluster = point.find_cluster(clusters)
            nearest_cluster.add_point(point)

        for cluster in clusters:
            cluster.recalculate()

    print(clusters.calculate_distortion())
    clusters.output_data()


if __name__ == "__main__":
    main()
