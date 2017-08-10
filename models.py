from scipy.interpolate import interp1d
from collections import OrderedDict
import matplotlib.pyplot as plt
import tinydb

class AirFoil():

    def __init__(self, description, x_points, y_positive, y_negative):
        self.coordinates = OrderedDict(
            zip(x_points, list(zip(y_positive, y_negative)))
        )
        self.description = description

    def __len__(self):
        return len(self.coordinates)

    def interpolate(self, x_points):
        "Take a list of points in the x axis and interpolate y values for it."
        needed_points = [
            point for point in x_points if point not in self.x_coordinates
        ]
        if not needed_points:
            return
        f_positive = interp1d(
            self.x_coordinates, self.y_coordinates_positive()
        )
        f_negative = interp1d(
            self.x_coordinates, self.y_coordinates_negative()
        )
        for point in needed_points:
            self.coordinates[point] = [
                float(f_positive(point)), float(f_negative(point))
            ]
        self.sort()

    def sort(self):
        """Will sort the AirFoil coordinates based on the x coordinate."""
        cords_list_to_sort = list(self.coordinates.items())
        cords_sorted_list = sorted(cords_list_to_sort)
        self.coordinates = OrderedDict(cords_sorted_list)

    @property
    def x_coordinates(self):
        x_points = []
        for x in self.coordinates:
            x_points.append(x)
        return x_points

    def y_coordinates(self, half='default'):
        y_list = []
        for x, y in self.coordinates.items():
            if half == 'positive':
                y_list.append(y[0])
            elif half == 'negative':
                y_list.append(y[1])
            else:
                y_list.append(list(y))
        return y_list

    def y_coordinates_positive(self):
        return self.y_coordinates('positive')

    def y_coordinates_negative(self):
        return self.y_coordinates('negative')

    def plot(self):
        plt.plot(self.x_coordinates, self.y_coordinates())
        plt.show()

    def save(self):
        pass
