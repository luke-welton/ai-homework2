# Implementation of k-means algorithm
from math import sqrt

class Point:
    def __init__(self, x=0.0, y=0.0):
        self.coordinates = (x, y)


    def calculate_distance(self, point):
        return sqrt((self.coordinates[0] - point[0]) ** 2 + (self.coordinates[1] - point[1]) ** 2)


class Cluster:
    def __init__(self):
        self.points = []
        self.means = [0, 0, 0]

    def add_point(self, x, y):
        self.points.append(Point(x, y))

    def calculate(self):

        #group each point to nearest k-mean

def main():
    means_cluster = Cluster()




if __name__ == "__main__":
    main()
