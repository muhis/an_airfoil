from scipy.interpolate import interp1d
from scipy.spatial.distance import cdist
import numpy as np
from collections import OrderedDict
import matplotlib.pyplot as plt
import tinydb
import logging


db = tinydb.TinyDB('airfoils.json')
objects = tinydb.Query()


class AirFoil():

    def __init__(self, description,
                 x_points, y_positive, y_negative, name='default'):
        self.coordinates = OrderedDict(
            zip(x_points, list(zip(y_positive, y_negative)))
        )
        self.description = description
        self.name = name

    def __len__(self):
        return len(self.coordinates)

    def interpolate(self, x_points):
        """
        Take a list of points in the x axis and interpolate y values for it.
        """
        needed_points = [
            point for point in x_points if point not in self.x_coordinates
        ]
        if not needed_points:
            return
        f_positive = interp1d(
            self.x_coordinates, self.y_coordinates_positive
        )
        f_negative = interp1d(
            self.x_coordinates, self.y_coordinates_negative
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

    @property
    def y_coordinates_positive(self):
        return self.y_coordinates('positive')

    @property
    def y_coordinates_negative(self):
        return self.y_coordinates('negative')

    def plot(self):
        plt.plot(self.x_coordinates, self.y_coordinates())
        plt.show()

    def as_dict(self):
        """Return dictionary of the airfoil."""
        return {
            'x_points': self.x_coordinates,
            'y_positive': self.y_coordinates_positive,
            'y_negative': self.y_coordinates_negative,
            'description': self.description,
            'name': self.name
        }

    def save(self, db=tinydb.TinyDB('airfoils.json')):
        """
        Save the airfoil object to the database.

        It will update the airfoil if the name is already available
        in the database. If the name is new, it will create it.
        """
        previous_object = db.contains(objects.name == self.name)
        if previous_object:
            db.remove(objects.name == self.name)
        # The object can not be found
        db.insert(
            {
                'name': self.name,
                'x_points': self.x_coordinates,
                'y_positive': self.y_coordinates_positive,
                'y_negative': self.y_coordinates_negative,
                'description': self.description
            }
        )
        pass


def equate(first_air_foil, second_air_foil):
    """Take two airfoil objects and interpolate both of them."""
    # Take copy of the x_coordinates before the change.
    first_airfoil_copy = first_air_foil.x_coordinates[:]
    second_air_foil_copy = second_air_foil.x_coordinates[:]
    first_air_foil.interpolate(second_air_foil_copy)
    second_air_foil.interpolate(first_airfoil_copy)


def distance_between_curves_std(first_curve, second_curve):
    """Return the distance between points in two curves(Standard deviation)."""
    # First we equate the two curves to have similar amount of points.
    if len(first_curve) != len(second_curve):
        raise Exception('The curves are not equal, equate airfoils first.')

    first_array = np.array(first_curve)
    second_array = np.array(second_curve)
    return (sum((first_array-second_array)**2)/3)**0.5


def airfoil_from_lednicer(data, name):
    middle_point = int((len(data) - 1) / 2) + 1
    # End of file.
    eof = len(data) - 1
    x = []
    y_positive = []
    y_negative = []
    # Get the first half of the file,
    # starting from 3 row until the middle point
    for row in data[3:middle_point]:
        try:
            # First item of the row is the x point,
            # the second is the positive y point.
            x.append(float(row.split()[0]))
            y_positive.append(float(row.split()[1]))
        except ValueError:
            pass
    # Get the second half of the file to get the negative y points.
    for row in data[(middle_point + 1):eof]:
        try:
            y_negative.append(float(row.split()[1]))
        except ValueError:
            pass
    return AirFoil(
        description=data[0], x_points=x,
        y_positive=y_positive, y_negative=y_negative,
        name=name
    )


def airfoil_from_selig(data, name):
    middle_point = int((len(data) - 1) / 2)
    # End of file
    eof = len(data) - 1
    x = []
    y_positive = []
    y_negative = []
    # Flipping coordinations, selig coordinates descends.
    flipped_first_half = data[middle_point::-1]
    for row in flipped_first_half[:-1]:
        try:
            x.append(float(row.split()[0]))
            y_positive.append(float(row.split()[1]))
        except ValueError:
            pass
    for row in data[middle_point:eof]:
        try:
            y_negative.append(float(row.split()[1]))
        except ValueError:
            pass
    return AirFoil(
        description=data[0], x_points=x,
        y_positive=y_positive, y_negative=y_negative,
        name=name
    )


def airfoil_from_data(input_data, name):
        # determine file format: selig or Lednicer
        third_line = input_data[2]
        if not(third_line):
            # The dat format is Lednicer.
            return airfoil_from_lednicer(input_data, name)
        else:
            # The dat format is selig.
            return airfoil_from_selig(input_data, name)


def airfoil_from_database(name, db=tinydb.TinyDB('airfoils.json')):
    """Return an airfoil object from database."""
    airfoil_attributes = db.get(objects.name == name)
    if airfoil_attributes:
        return AirFoil(**airfoil_attributes)
    else:
        raise LookupError(
            'The AirFoil %s can not be found in the database %s' %
            name,
            db
        )


def populate_db_from_zip(zip_path,  db=tinydb.TinyDB('airfoils.json')):
    """Parse zip archive and convert each file to an entry in the databas."""
    import zipfile
    if not zipfile.is_zipfile(zip_path):
        raise zipfile.BadZipFile(
            'Zip file in path %s can not be parsed' %
            zip_path
        )
    with zipfile.ZipFile(zip_path, mode='r') as zip_object:
        air_foils_list = []
        for name in zip_object.namelist():
            try:
                airfoil_file = zip_object.read(name).decode('utf8').split('\n')
                if len(airfoil_file) < 2:
                    continue
                airfoil_name = name.split('/')[1].split('.')[0]

                air_foil = airfoil_from_data(
                    name=airfoil_name,
                    input_data=airfoil_file
                )
                air_foils_list.append(air_foil.as_dict())
            except Exception:
                print('Failed while trying parsing %s with exception.' % name)
        try:
            db.insert_multiple(air_foils_list)
        except Exception:
            print('Failed while inserting the airfoils into the databse')


def compare_airfoils(main_air_foil, comparison_airfoils):
    """Return a dictionary of the results of std comparison."""
    results = {}
    for air_foil in comparison_airfoils:
        main_airfoil_copy = AirFoil(
            name='copy',
            x_points=main_air_foil.x_coordinates[:],
            y_positive=main_air_foil.y_coordinates_positive[:],
            y_negative=main_air_foil.y_coordinates_negative[:],
            description='copy'
        )
        equate(main_airfoil_copy, air_foil)
        y_pos_distance = distance_between_curves_std(
            main_air_foil.y_coordinates_positive,
            air_foil.y_coordinates_positive
        )
        y_neg_distance = distance_between_curves_std(
            main_air_foil.y_coordinates_positive,
            air_foil.y_coordinates_negative
        )
        results[air_foil.name] = (
            (y_pos_distance ** 2) + (y_neg_distance ** 2)
        ) ** 2
        return results
