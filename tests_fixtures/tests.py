"""Tests for an_airfoil main functionalities."""
import unittest
from converters import wing_from_data as wfd
from equity import equate

class TestWings(unittest.TestCase):
    def test_wings_load(self):
        """
        Test if wings loading works as expected
        """
        pass

    def test_wing_from_selig(self):
        """Test that selig format can be parsed to functional objects"""
        f = open('test_sample/selig.txt').read().split('\n')
        return wfd(f)

    def test_wing_from_lednicer(self):
        """Test that selig format can be parsed to functional objects"""
        lednicer_file = open('test_sample/lednicer.txt').read().split('\n')
        import ipdb; ipdb.set_trace()
        return wfd(f)


if __name__ == '__main__':
    unittest.main()

def test():
    input_file = input('Please input file name: ')
    f = open(input_file, 'r').read().split('\n')
    return wfd(f)



def test4():
    wing1 = test2()
    wing2 = test3()
    return equate(wing1, wing2)
