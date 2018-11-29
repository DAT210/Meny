from flask import Flask, render_template, send_from_directory, g, Blueprint, current_app
import os
import mysql.connector
import socket
from get_functions import *
import json

app = Flask(__name__)
app.debug = True
# app.debug = True

# CHANGE THIS INFORMATION FOR YOUR DATABASE ACCESS OK
user_info = {
    "username": "root",
    "password": "root",
    "database": "dat210_menu",
    "hostname": "mysql",
}


app.config["DATABASE_USER"] = user_info["username"]
app.config["DATABASE_PASSWORD"] = user_info["password"]
app.config["DATABASE_DB"] = user_info["database"]
app.config["DATABASE_HOST"] = user_info["hostname"]
app.debug = True


def get_db():
    if not hasattr(g, "_database"):
        g._database = mysql.connector.connect(
            host=app.config["DATABASE_HOST"],
            user=app.config["DATABASE_USER"],
            password=app.config["DATABASE_PASSWORD"],
            database=app.config["DATABASE_DB"]
        )
    return g._database


@app.teardown_appcontext
def teardown_db(error):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()
        
@app.route("/",methods=["GET"])
def index():
    db = get_db()
    courses = get_courses(db)
    categories = {}   
    try:
        for category in get_categories(db):
            ca_id = category["ca_id"]
            if ca_id not in categories:
                categories[ca_id] = category["ca_name"]
        # Sort the courses by category
        course_categories = {}
        for course in courses:
            # Link name to id for the category
            category = categories[course["ca_id"]]
            if category in course_categories:
                course_categories[category].append(course)
            else:
                course_categories[category] = [course]
        
        patoMenu = {
            "Starters":course_categories["Starters"],
            "Drinks":course_categories["Drinks"],
            "Main":course_categories["Main"],
            "Desert":course_categories["Dessert"],
        }
        
        alternateMenu = {
            "Lunch":course_categories["Lunch"],
            "Dinner":course_categories["Dinner"],
        }
    except Error as err:
        return err

    return json.dumps({"patoMenu":patoMenu,"alternateMenu":alternateMenu})
 
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)