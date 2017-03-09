from scipy.interpolate import interp1d
from collections import OrderedDict
import matplotlib.pyplot as plt
class Wings():

    def __init__(self, description, x_points, y_positive, y_negative):
        self.coordinates = OrderedDict(zip(x_points, list(zip(y_positive, y_negative))))
        self.description = description


    def __len__(self):
        return len(self.coordinates)

    def interpolate(self, x_point):
        f_positive = interp1d(self.x_coordinates(), self.y_coordinates_positive())
        f_negative = interp1d(self.x_coordinates(), self.y_coordinates_negative())
        self.coordinates[x_point] = [float(f_positive(x_point)),float(f_negative(x_point))]
        self.sort()

    def sort(self):
        cords_list_to_sort = list(self.coordinates.items())
        cords_sorted_list = sorted(cords_list_to_sort)
        self.coordinates = OrderedDict(cords_sorted_list)

    def x_coordinates(self):
        x_points = []
        for x in self.coordinates:
            x_points.append(x)
        return x_points

    def y_coordinates(self, half = 'default'):
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
        plt.plot(self.x_coordinates(), self.y_coordinates())
        plt.show()
        
