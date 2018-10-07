from flask import render_template
from exceptions import *
import types
import mysql.connector
from mysql.connector import IntegrityError, DataError, Error

# Magnus Steinstø


insert_queries = {
    "insert_course": "INSERT INTO course (c_name, price) VALUES ('{c_name}', '{price}')",

    "insert_ingredient": "INSERT INTO ingredient (i_name, available) VALUES ('{i_name}', {available})",

    "insert_allergene": "INSERT INTO allergene (a_name) VALUES ('{a_name}')",

    "insert_course_ingredient": "INSERT INTO course_ingredient (c_id, i_id) VALUES ({c_id}, {i_id})",

    "insert_ingredient_allergene": "INSERT INTO ingredient_allergene (i_id, a_id) VALUES ({i_id}, {a_id})"
}

def insert_course(db, c_name, price):
    cur = db.cursor()
    try:
        if c_name == None or price == None:
            return EMPTY_INPUT_EXCEPTION
        cur.execute(insert_queries["insert_course"].replace("{c_name}", c_name).replace("{price}", str(price)))
        db.commit()
    except (IntegrityError):
        return DUPLICATE_VALUE_EXCEPTION
    except (DataError):
        return INPUT_TOO_LONG_EXCEPTION
    except (Error) as err:
        if 'Incorrect decimal value' in str(err):
            return INVALID_DECIMAL_VALUE
        raise err
    finally:
        cur.close()


def insert_ingredient(db, i_name, available):
    cur = db.cursor()
    try:
        if i_name == None or available == None:
            return EMPTY_INPUT_EXCEPTION
        cur.execute(insert_queries["insert_ingredient"].replace("{i_name}", i_name).replace("{available}", str(available)))
        db.commit()
    except (IntegrityError):
        return DUPLICATE_VALUE_EXCEPTION
    except (DataError):
        return INPUT_TOO_LONG_EXCEPTION
    except Error as err:
        if 'Unknown column' in str(err):
            return INVALID_TYPE_EXCEPTION
        print(str(err))
    finally:
        cur.close()

def insert_allergene(db, a_name):
    cur = db.cursor()
    try:
        if a_name == None:
            return EMPTY_INPUT_EXCEPTION
        cur.execute(insert_queries["insert_allergene"].replace("{a_name}", a_name))
        db.commit()
    except (IntegrityError):
        return DUPLICATE_VALUE_EXCEPTION
    except (DataError):
        return INPUT_TOO_LONG_EXCEPTION
    finally:
        cur.close()


def insert_course_ingredient(db, c_id, i_id):
    cur = db.cursor()
    try:
        if c_id == None or i_id == None:
            return EMPTY_INPUT_EXCEPTION
        cur.execute(insert_queries["insert_course_ingredient"].replace("{c_id}", str(c_id)).replace("{i_id}", str(i_id)))
        db.commit()
    except Error as err:
        if 'Cannot add or update a child row: a foreign key constraint fails' in str(err):
            return UNKKNOWN_REFERENCE_EXCEPTION
        if 'Unknown column' in str(err):
            return INVALID_TYPE_EXCEPTION
        raise err
    finally:
        cur.close()


def insert_ingredient_allergene(db, i_id, a_id):
    cur = db.cursor()
    try:
        if i_id == None or a_id == None:
            return EMPTY_INPUT_EXCEPTION
        cur.execute(insert_queries["insert_ingredient_allergene"].replace("{i_id}", str(i_id)).replace("{a_id}", str(a_id)))
        db.commit()
    except Error as err:
        if 'Cannot add or update a child row: a foreign key constraint fails' in str(err):
            return UNKKNOWN_REFERENCE_EXCEPTION
        if 'Unknown column' in str(err):
            return INVALID_TYPE_EXCEPTION
        raise err
    finally:
        cur.close()