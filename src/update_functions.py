from flask import render_template
import types
import mysql.connector
from mysql.connector import IntegrityError, DataError, Error

update_queries = {
    # ------------------------ Course ------------------------
    # Update course name by id
    "update_course_name": "UPDATE course SET c_name='{c_name}' WHERE c_id={c_id}",

    # Update course price by id
    "update_course_price": "UPDATE course SET price='{price}' WHERE c_id={c_id}",

    # ------------------------ Ingredient ------------------------
    # Update ingredient name by id
    "update_ingredient_name": "UPDATE ingredient SET i_name='{i_name}' WHERE i_id={i_id}",

    # Update ingredient availability by id
    "update_ingredient_availability": "UPDATE ingredient SET available={available} WHERE i_id={i_id}",

    # ------------------------ Allergene ------------------------
    # Update allergene name by id
    "update_allergene_name": "UPDATE allergene SET a_name='{a_name}' WHERE a_id={a_id}",
}

def update_course_name(db, c_name, c_id):
    cur = db.cursor()
    if c_name == None or c_id == None:
        raise TypeError('The inputs can not contain an empty value')
    cur.execute(update_queries["update_course_name"].replace("{c_name}", c_name).replace("{c_id}", str(c_id)))
    db.commit()
    if cur.rowcount == 0:
        # An update went by without changing any values
        raise Error('No row found by id')
    cur.close()


def update_course_price(db, price, c_id):
    cur = db.cursor()
    if price == None or c_id == None:
        raise TypeError('The inputs can not contain an empty value')
    cur.execute(update_queries["update_course_price"].replace("{price}", str(price)).replace("{c_id}", str(c_id)))
    db.commit()
    if cur.rowcount == 0:
        # An update went by without changing any values
        raise Error('No row found by id')
    cur.close()


def update_ingredient_name(db, i_name, i_id):
    cur = db.cursor()
    if i_name == None or i_id == None:
        raise TypeError('The inputs can not contain an empty value')
    cur.execute(update_queries["update_ingredient_name"].replace("{i_name}", i_name).replace("{i_id}", str(i_id)))
    db.commit()
    if cur.rowcount == 0:
        # An update went by without changing any values
        raise Error('No row found by id')
    cur.close()


def update_ingredient_availability(db, available, i_id):
    cur = db.cursor()
    if available == None or i_id == None:
        raise TypeError('The inputs can not contain an empty value')
    if not (type(available) == bool):
        raise TypeError('Available is not of type boolean')
    cur.execute(update_queries["update_ingredient_availability"].replace("{available}", str(available)).replace("{i_id}", str(i_id)))
    db.commit()
    if cur.rowcount == 0:
        # An update went by without changing any values
        raise Error('No row found by id')
    cur.close()


def update_allergene_name(db, a_name, a_id):
    cur = db.cursor()
    if a_name == None or a_id == None:
        raise TypeError('The inputs can not contain an empty value')
    cur.execute(update_queries["update_allergene_name"].replace("{a_name}", a_name).replace("{a_id}", str(a_id)))
    db.commit()
    if cur.rowcount == 0:
        # An update went by without changing any values
        raise Error('No row found by id')
    cur.close()