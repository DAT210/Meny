import unittest
import update_functions
import get_functions
import test_database
import mysql.connector
from exceptions import *
from get_functions import *
from mysql.connector import errorcode, IntegrityError, DataError, Error

# Magnus Steinstø

expected_return_values = {
    "get_courses": "[{'c_id': '1', 'c_name': 'course alpha', 'price': '5.20', 'ingredients': [{'i_id': '1', 'i_name': 'ingredient alpha', 'available': '1', 'allergenes': [{'a_id': '2', 'a_name': 'allergene bravo'}, {'a_id': '3', 'a_name': 'allergene charlie'}]}, {'i_id': '3', 'i_name': 'ingredient charlie', 'available': '1', 'allergenes': []}]}, {'c_id': '2', 'c_name': 'course bravo', 'price': '4.20', 'ingredients': [{'i_id': '1', 'i_name': 'ingredient alpha', 'available': '1', 'allergenes': [{'a_id': '2', 'a_name': 'allergene bravo'}, {'a_id': '3', 'a_name': 'allergene charlie'}]}, {'i_id': '2', 'i_name': 'ingredient bravo', 'available': '1', 'allergenes': [{'a_id': '3', 'a_name': 'allergene charlie'}]}, {'i_id': '5', 'i_name': 'ingredient echo', 'available': '1', 'allergenes': []}]}, {'c_id': '3', 'c_name': 'course charlie', 'price': '3.75', 'ingredients': [{'i_id': '1', 'i_name': 'ingredient alpha', 'available': '1', 'allergenes': [{'a_id': '2', 'a_name': 'allergene bravo'}, {'a_id': '3', 'a_name': 'allergene charlie'}]}, {'i_id': '3', 'i_name': 'ingredient charlie', 'available': '1', 'allergenes': []}]}, {'c_id': '4', 'c_name': 'course delta', 'price': '2.10', 'ingredients': [{'i_id': '1', 'i_name': 'ingredient alpha', 'available': '1', 'allergenes': [{'a_id': '2', 'a_name': 'allergene bravo'}, {'a_id': '3', 'a_name': 'allergene charlie'}]}, {'i_id': '5', 'i_name': 'ingredient echo', 'available': '1', 'allergenes': []}]}, {'c_id': '5', 'c_name': 'course echo', 'price': '7.40', 'ingredients': [{'i_id': '1', 'i_name': 'ingredient alpha', 'available': '1', 'allergenes': [{'a_id': '2', 'a_name': 'allergene bravo'}, {'a_id': '3', 'a_name': 'allergene charlie'}]}, {'i_id': '2', 'i_name': 'ingredient bravo', 'available': '1', 'allergenes': [{'a_id': '3', 'a_name': 'allergene charlie'}]}, {'i_id': '3', 'i_name': 'ingredient charlie', 'available': '1', 'allergenes': []}]}]",
    "get_ingredients": "[{'i_id': '1', 'i_name': 'ingredient alpha', 'available': '1', 'allergenes': [{'a_id': '2', 'a_name': 'allergene bravo'}, {'a_id': '3', 'a_name': 'allergene charlie'}]}, {'i_id': '2', 'i_name': 'ingredient bravo', 'available': '1', 'allergenes': [{'a_id': '3', 'a_name': 'allergene charlie'}]}, {'i_id': '3', 'i_name': 'ingredient charlie', 'available': '1', 'allergenes': []}, {'i_id': '4', 'i_name': 'ingredient delta', 'available': '1', 'allergenes': []}, {'i_id': '5', 'i_name': 'ingredient echo', 'available': '1', 'allergenes': []}]",
    "get_ingredients_by_course": "[{'i_id': '1', 'i_name': 'ingredient alpha', 'available': '1', 'allergenes': [{'a_id': '2', 'a_name': 'allergene bravo'}, {'a_id': '3', 'a_name': 'allergene charlie'}]}, {'i_id': '3', 'i_name': 'ingredient charlie', 'available': '1', 'allergenes': []}]",
    "get_allergens_by_ingredient": "[{'a_id': '2', 'a_name': 'allergene bravo'}, {'a_id': '3', 'a_name': 'allergene charlie'}]"
}

def get_db():
    return mysql.connector.connect(user='root', password='root',
                                host='127.0.0.1',
                                database='test_menu')


class TestGetFunctions(unittest.TestCase):

    def setUp(self):
        # Called before each test
        test_database.create_test_db()


    def tearDown(self):
        # Called after every test
        test_database.drop_test_db()

    def test_get_courses(self):
        db = get_db()

        # Get values and compare to expected results
        courses = get_courses(db)
        self.assertEqual(str(courses), expected_return_values["get_courses"])
        db.close()


    def test_get_ingredients(self):
        db = get_db()

        # Get values and compare to expected results
        ingredients = get_ingredients(db)
        self.assertEqual(str(ingredients), expected_return_values["get_ingredients"])
        db.close()


    def test_get_ingredients_by_course(self):
        db = get_db()

        # Get values and compare to expected results
        ingredients = get_ingredients_by_course(db, 1)
        self.assertEqual(str(ingredients), expected_return_values["get_ingredients_by_course"])

        # Get with non-existing id (should return empty set)
        self.assertEqual(get_ingredients_by_course(db, 999), [])

        # Get with invalid input id
        self.assertEqual(get_ingredients_by_course(db, "a"),
                         INVALID_TYPE_EXCEPTION)

        # Get with empty id value
        self.assertEqual(get_ingredients_by_course(db, None),
                         EMPTY_INPUT_EXCEPTION)
        db.close()


    def test_get_allergenes_by_ingredient(self):
        db = get_db()

        # Get values and compare to expected results
        allergens = get_allergenes_by_ingredient(db, 1)
        self.assertEqual(str(allergens), expected_return_values["get_allergens_by_ingredient"])

        # Get with non-existing id (should return empty set)
        self.assertEqual(get_allergenes_by_ingredient(db, 999), [])

        # Get with invalid input id
        self.assertEqual(get_allergenes_by_ingredient(db, "a"),
                         INVALID_TYPE_EXCEPTION)

        # Get with empty id value
        self.assertEqual(get_allergenes_by_ingredient(db, None),
                         EMPTY_INPUT_EXCEPTION)
        db.close()


if __name__ == '__main__':
    unittest.main()
