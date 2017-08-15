"""Tests for an_airfoil main functionalities."""
import unittest
from models import airfoil_from_data as afd
from models import (
    AirFoil, airfoil_from_database, populate_db_from_zip, equate,
    distance_between_curves_std,
    compare_airfoils
)
from tinydb import TinyDB, Query
objects = Query()


class TestAirFoil(unittest.TestCase):
    """Tests for AirFoil class and methods."""
    def setUp(self):
        """Construct test needed objects."""
        from tinydb.storages import MemoryStorage
        self.test_db = TinyDB(storage=MemoryStorage)

    def test_airfoil_from_db(self):
        """Test if wings loading from db works as expected."""
        air_foil_attributes = {
            'name': 'test',
            'x_points': [1, 2, 3, 4],
            'y_positive': [0.1, 0.2, 0.3, 0.4],
            'y_negative': [10, 20, 30, 40],
            'description': 'description_test'
        }
        self.test_db.insert(air_foil_attributes)
        airfoil_object = airfoil_from_database(name='test', db=self.test_db)
        self.assertEqual(
            airfoil_object.x_coordinates, air_foil_attributes['x_points']
        )
        self.assertEqual(
            airfoil_object.y_coordinates_positive,
            air_foil_attributes['y_positive']
        )
        self.assertEqual(
            airfoil_object.y_coordinates_negative,
            air_foil_attributes['y_negative']
        )

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
        air_foil = afd(selig_file, 'Test')
        self.assertEqual(air_foil.x_coordinates, fixture_x_coordinates)

    def test_wing_from_lednicer(self):
        """Test that lednicer format can be parsed to functional objects."""
        with open('tests_fixtures/lednicer.txt') as f:
            lednicer_file = f.read().split('\n')
        air_foil = afd(lednicer_file, name='Tesst')
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
                airfoils[air_foil_name] = afd(airfoil_file, name=file_name)
        equate(airfoils['first'], airfoils['second'])
        self.assertEqual(
            airfoils['first'].x_coordinates,
            airfoils['second'].x_coordinates
        )
        airfoils['first'].save()
        airfoils['second'].save()

    def test_save_new_object(self):
        """When the object name is new, new object in db should be created."""
        test_airfoil = AirFoil(
            name='test',
            x_points=[1, 2, 3, 4],
            y_positive=[0.1, 0.2, 0.3, 0.4],
            y_negative=[10, 20, 30, 40],
            description='description_test'
        )
        test_airfoil.save(db=self.test_db)
        airfoil_attribs_from_db = self.test_db.get(objects.name == 'test')
        self.assertEqual(
            test_airfoil.x_coordinates,
            airfoil_attribs_from_db['x_points']
        )
        self.assertEqual(
            test_airfoil.y_coordinates_positive,
            airfoil_attribs_from_db['y_positive']
        )
        self.assertEqual(
            test_airfoil.y_coordinates_negative,
            airfoil_attribs_from_db['y_negative']
        )

    def test_save_for_old_object(self):
        """When the object name is old, old object should be updated."""
        # Create an intry in the database with the name test.
        self.test_db.insert({'name': 'test', 'x_points': [0, 0, 0]})
        test_airfoil = AirFoil(
            name='test',
            x_points=[1, 2, 3, 4],
            y_positive=[0.1, 0.2, 0.3, 0.4],
            y_negative=[10, 20, 30, 40],
            description='description_test'
        )
        test_airfoil.save(db=self.test_db)
        airfoil_attribs_from_db = self.test_db.get(objects.name == 'test')
        self.assertEqual(
            test_airfoil.x_coordinates,
            airfoil_attribs_from_db['x_points']
        )
        self.assertEqual(
            test_airfoil.y_coordinates_positive,
            airfoil_attribs_from_db['y_positive']
        )
        self.assertEqual(
            test_airfoil.y_coordinates_negative,
            airfoil_attribs_from_db['y_negative']
        )

    def tearDown(self):
        """Delete test objects from test database."""
        self.test_db.purge()


class TestBuildFromZip(unittest.TestCase):
    """Build the database from a zip file."""

    def setUp(self):
        """Construct test needed objects."""
        from tinydb.storages import MemoryStorage
        self.test_db = TinyDB(storage=MemoryStorage)

    def test_build_db(self):
        """Test that the zip file is correctly parsed and saved"""
        path = 'tests_fixtures/test.zip'
        populate_db_from_zip(zip_path=path, db=self.test_db)
        selig_object = self.test_db.get(objects.name == 'selig')
        bng_object = self.test_db.get(objects.name == 'bng')
        self.assertIsNotNone(selig_object)
        self.assertIsNotNone(bng_object)
        self.assertEqual(len(selig_object['x_points']), 35)
        self.assertEqual(len(bng_object['x_points']), 11)

    def test_bad_zip(self):
        """If the zip not given an archive, it should raise an exception"""
        import zipfile
        with self.assertRaises(zipfile.BadZipFile):
            populate_db_from_zip(zip_path='test.py')


class TestDistance(unittest.TestCase):
    """Test the functions related to distance calculation."""

    def setUp(self):
        """Construct test needed objects."""
        from tinydb.storages import MemoryStorage
        self.test_db = TinyDB(storage=MemoryStorage)
        path = 'tests_fixtures/test.zip'
        populate_db_from_zip(zip_path=path, db=self.test_db)
        self.fixture_airfoils = [
            airfoil_from_database('selig', db=self.test_db),
            airfoil_from_database('bng', db=self.test_db)
        ]

    def test_not_equal_curves(self):
        """The function should not accept unequal curves."""
        with self.assertRaises(Exception):
            distance_between_curves_std(
                [1, 2, 3], [1, 2, 3, 4]
            )

    def test_distance_std(self):
        """Test stadnard deviation distance between two curves."""
        distance = distance_between_curves_std(
            [1, 2, 3, 4], [1.5, 2.5, 3.5, 4.5]
        )
        self.assertEqual(distance, 0.57735026918962573)

    def test_compare_airfoils(self):
        """Test the function compare airfoils."""
        compare_results = compare_airfoils(
            self.fixture_airfoils[0], self.fixture_airfoils
        )
        result_fixture = {
            'selig': 0.0018230416652564628
        }
        self.assertEqual(compare_results, result_fixture)


if __name__ == '__main__':
    unittest.main()
