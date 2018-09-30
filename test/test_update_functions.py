import unittest
import update_functions
import get_functions
import test_database
import mysql.connector
from mysql.connector import errorcode, IntegrityError, DataError, Error


def get_db():
    return mysql.connector.connect(user='root', password='root',
                                host='127.0.0.1',
                                database='test_menu')


class TestUpdateFunctions(unittest.TestCase):

    def setUp(self):
        # Called before each test
        test_database.create_test_db()


    def tearDown(self):
        # Called after every test
        test_database.drop_test_db()


    def test_update_course_name(self):
        db = get_db()
        # Valid input
        update_functions.update_course_name(db, "update course alpha", 1)
        cur = db.cursor()
        try:
            cur.execute("SELECT c_name FROM course WHERE c_id=1")
            name = cur.fetchone()[0]
        except Error as err:
            return err
        finally:
            cur.close()
        self.assertEqual("update course alpha", name)

        # Update name to existing name (name must be unique)
        with self.assertRaises(IntegrityError) as context:
            update_functions.update_course_name(db, "course charlie", 2)
        self.assertTrue('Duplicate entry' in str(context.exception))

        # Update name to invalid value
        with self.assertRaises(DataError) as context:
            update_functions.update_course_name(db, "asdfasdfasdfasdfasdfasdfasdfasdfasfdasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdf", 4)
        self.assertTrue('Data too long for column' in str(context.exception))

        # Update name with non-existing id
        with self.assertRaises(Error) as context:
            update_functions.update_course_name(db, "course id out of bound", 999)
        self.assertTrue('No row found by id' in str(context.exception))

        # Update name to empty value
        with self.assertRaises(TypeError) as context:
            update_functions.update_course_name(db, None, 2)
        self.assertTrue('The inputs can not contain an empty value' in str(context.exception))

        # Update name with empty id
        with self.assertRaises(TypeError) as context:
            update_functions.update_course_name(db, "valid input", None)
        self.assertTrue('The inputs can not contain an empty value' in str(context.exception))

        db.close()

    def test_update_course_price(self):
        db = get_db()
        # Valid input
        update_functions.update_course_price(db, 5.55, 1)
        cur = db.cursor()
        try:
            cur.execute("SELECT price FROM course WHERE c_id=1")
            price = cur.fetchone()[0]
        except Error as err:
            return err
        finally:
            cur.close()
        self.assertEqual(str(5.55), str(price))

        # Update price to invalid value
        with self.assertRaises(Error) as context:
            update_functions.update_course_price(db, "asdfasdfasd", 4)
        self.assertTrue('Incorrect decimal value' in str(context.exception))

        # Update price with non-existing id
        with self.assertRaises(Error) as context:
            update_functions.update_course_price(db, 8.89, 999)
        self.assertTrue('No row found by id' in str(context.exception))

        # Update price to empty value
        with self.assertRaises(TypeError) as context:
            update_functions.update_course_price(db, None, 2)
        self.assertTrue('The inputs can not contain an empty value' in str(context.exception))

        # Update price with empty id
        with self.assertRaises(TypeError) as context:
            update_functions.update_course_price(db, 4.34, None)
        self.assertTrue('The inputs can not contain an empty value' in str(context.exception))

        db.close()

    def test_update_ingredient_name(self):
        db = get_db()
        # Valid input
        update_functions.update_ingredient_name(db, "update ingredient alpha", 1)
        cur = db.cursor()
        try:
            cur.execute("SELECT i_name FROM ingredient WHERE i_id=1")
            name = cur.fetchone()[0]
        except Error as err:
            return err
        finally:
            cur.close()
        self.assertEqual("update ingredient alpha", name)

        # Update name to existing name (name must be unique)
        with self.assertRaises(IntegrityError) as context:
            update_functions.update_ingredient_name(db, "ingredient charlie", 2)
        self.assertTrue('Duplicate entry' in str(context.exception))

        # Update name to invalid value
        with self.assertRaises(DataError) as context:
            update_functions.update_ingredient_name(db,
                                                "asdfasdfasdfasdfasdfasdfasdfasdfasfdasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdf",
                                                4)
        self.assertTrue('Data too long for column' in str(context.exception))

        # Update name with non-existing id
        with self.assertRaises(Error) as context:
            update_functions.update_ingredient_name(db, "course id out of bound", 999)
        self.assertTrue('No row found by id' in str(context.exception))

        # Update name to empty value
        with self.assertRaises(TypeError) as context:
            update_functions.update_ingredient_name(db, None, 2)
        self.assertTrue('The inputs can not contain an empty value' in str(context.exception))

        # Update name with empty id
        with self.assertRaises(TypeError) as context:
            update_functions.update_ingredient_name(db, "valid input", None)
        self.assertTrue('The inputs can not contain an empty value' in str(context.exception))

        db.close()


    def test_update_ingredient_availability(self):
        db = get_db()
        # Valid input
        update_functions.update_ingredient_availability(db, False, 1)
        cur = db.cursor()
        try:
            cur.execute("SELECT available FROM ingredient WHERE i_id=1")
            available = cur.fetchone()[0]
        except Error as err:
            return err
        finally:
            cur.close()
        self.assertEqual(False, available)

        # Update available to invalid value
        with self.assertRaises(TypeError) as context:
            update_functions.update_ingredient_availability(db, "a", 4)
        self.assertTrue('Available is not of type boolean' in str(context.exception))

        # Update availability with non-existing id
        with self.assertRaises(Error) as context:
            update_functions.update_ingredient_availability(db, False, 999)
        self.assertTrue('No row found by id' in str(context.exception))

        # Update name to empty value
        with self.assertRaises(TypeError) as context:
            update_functions.update_ingredient_availability(db, None, 2)
        self.assertTrue('The inputs can not contain an empty value' in str(context.exception))

        # Update name with empty id
        with self.assertRaises(TypeError) as context:
            update_functions.update_ingredient_availability(db, True, None)
        self.assertTrue('The inputs can not contain an empty value' in str(context.exception))

        db.close()


    def test_update_allergene_name(self):
        db = get_db()
        # Valid input
        update_functions.update_allergene_name(db, "update allergene alpha", 1)
        cur = db.cursor()
        try:
            cur.execute("SELECT a_name FROM allergene WHERE a_id=1")
            name = cur.fetchone()[0]
        except Error as err:
            return err
        finally:
            cur.close()
        self.assertEqual("update allergene alpha", name)

        # Update name to existing name (name must be unique)
        with self.assertRaises(IntegrityError) as context:
            update_functions.update_allergene_name(db, "allergene charlie", 2)
        self.assertTrue('Duplicate entry' in str(context.exception))

        # Update name to invalid value
        with self.assertRaises(DataError) as context:
            update_functions.update_allergene_name(db,
                                                    "asdfasdfasdfasdfasdfasdfasdfasdfasfdasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdf",
                                                    4)
        self.assertTrue('Data too long for column' in str(context.exception))

        # Update name with non-existing id
        with self.assertRaises(Error) as context:
            update_functions.update_allergene_name(db, "course id out of bound", 999)
        self.assertTrue('No row found by id' in str(context.exception))

        # Update name to empty value
        with self.assertRaises(TypeError) as context:
            update_functions.update_allergene_name(db, None, 2)
        self.assertTrue('The inputs can not contain an empty value' in str(context.exception))

        # Update name with empty id
        with self.assertRaises(TypeError) as context:
            update_functions.update_allergene_name(db, "valid input", None)
        self.assertTrue('The inputs can not contain an empty value' in str(context.exception))

        db.close()







if __name__ == '__main__':
    unittest.main()


