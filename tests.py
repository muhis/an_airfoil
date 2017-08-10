"""Tests for an_airfoil main functionalities."""
import unittest
from converters import airfoil_from_data as afd
from equity import equate


class TestAirFoil(unittest.TestCase):
    """Tests for AirFoil class and methods."""

    def test_wings_load(self):
        """Test if wings loading works as expected."""
        pass

    def test_wing_from_selig(self):
        """Test that selig format can be parsed to functional objects."""
        with open('tests_fixtures/selig.txt') as f:
            selig_file = f.read().split('\n')
        fixture_x_coordinates = [
            0.0, 0.00107, 0.00428, 0.00961,
            0.01704, 0.02653, 0.03806, 0.05156, 0.06699, 0.08427,
            0.10332, 0.12408, 0.14645, 0.17033, 0.19562, 0.22221,
            0.25, 0.27886, 0.30866, 0.33928, 0.37059, 0.43474, 0.5,
            0.56526, 0.62941, 0.69134, 0.75, 0.80438, 0.85355, 0.89668,
            0.93301, 0.96194, 0.98296, 0.99572, 1.0
        ]
        air_foil = afd(selig_file)
        self.assertEqual(air_foil.x_coordinates, fixture_x_coordinates)

    def test_wing_from_lednicer(self):
        """Test that lednicer format can be parsed to functional objects."""
        with open('tests_fixtures/lednicer.txt') as f:
            lednicer_file = f.read().split('\n')
        air_foil = afd(lednicer_file)
        fixture_x_coordinates = [0.0, 0.00107, 0.00428, 0.00961, 0.01704, 1.0]
        self.assertEqual(air_foil.x_coordinates, fixture_x_coordinates)

    def test_equate(self):
        """
        Test the output of the equate function.

        When two airfoil objects get equated, they should both have the same
        points on the x axis
        """
        airfoils = {}
        files = {'first': 'selig.txt', 'second': 'bng.txt'}
        for air_foil_name, file_name in files.items():
            with open('tests_fixtures/%s' % file_name) as f:
                airfoil_file = f.read().split('\n')
                airfoils[air_foil_name] = afd(airfoil_file)
        equate(airfoils['first'], airfoils['second'])
        self.assertEqual(
            airfoils['first'].x_coordinates,
            airfoils['second'].x_coordinates
        )

if __name__ == '__main__':
    unittest.main()

def test():
    input_file = input('Please input file name: ')
    f = open(input_file, 'r').read().split('\n')
    return afd(f)



def test4():
    wing1 = test2()
    wing2 = test3()
    return equate(wing1, wing2)
