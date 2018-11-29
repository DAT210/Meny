from flask import Flask, render_template, send_from_directory, g, request, json
import os
import mysql.connector
import socket
from get_functions import *

app = Flask(__name__)
app.debug = True
# app.debug = True

# CHANGE THIS INFORMATION FOR YOUR DATABASE ACCESS OK
user_info = {
    "username": "root",
    "password": "MySQLNetty6",
    "database": "menu",
    "hostname": "localhost"
}


app.config["DATABASE_USER"] = user_info["username"]
app.config["DATABASE_PASSWORD"] = user_info["password"]
app.config["DATABASE_DB"] = user_info["database"]
app.config["DATABASE_HOST"] = user_info["hostname"]


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

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/menu")
def menu():
    db = get_db()
    courses = get_courses(db)
    categories = {}
    for category in get_categories(db):
        ca_id = category["ca_id"]
        if ca_id not in categories:
            categories[ca_id] = category["ca_name"]
    print(str(categories))
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
    print(patoMenu)

    selectioncategories = get_selection_categories(db)
    return render_template("menu.html",patoMenu=patoMenu, alternateMenu=alternateMenu, selectioncategories = selectioncategories)


@app.route("/getcourseinfo")
def getcourseinfo():
    courseid = request.args.get("course_id", None)
    db = get_db()
    courseinfo = get_course_by_id(db, courseid, True)
    jsoncourseinfo = json.dumps(courseinfo)
    return jsoncourseinfo


@app.route("/getcourseselection")
def getcourseselection():
    courseid = request.args.get("course_id",None)
    print(courseid)
    db = get_db()
    selections = get_selections_by_course(db,courseid)
    print(selections)

    if len(selections) == 0:    #no selections means nothing to edit
        return json.dumps(selections)
    else:


        ingredients = get_ingredients(db)
        print(ingredients)

        selectioncategory = get_selection_categories(db)
        print(selectioncategory)
        selectionlist = []

        for idx in range(len(selections)):
            totalinfo = {}
            selection = selections[idx]
            totalinfo = {"s_id":selection["s_id"],"s_name":selection["s_name"],"s_price":selection["s_price"]}
            for ing in range(len(ingredients)):
                ingredient = ingredients[ing]
                if ingredient["i_id"] == selection["i_id"]:
                    totalinfo["ingredient"] = {"i_id":ingredient["i_id"],"i_name":ingredient["i_name"],"available":ingredient["available"]}
            for cat in range(len(selectioncategory)):
                category = selectioncategory[cat]
                if category["sc_id"] == selection["sc_id"]:
                    totalinfo["sc_id"] = category["sc_id"]
                    totalinfo["sc_name"] = category["sc_name"]
            selectionlist.append(totalinfo)
        print(selectionlist)
        jsonobj = json.dumps(selectionlist)
        return jsonobj

@app.route("/getselectioncategory")
def getselectioncategory():
    db = get_db()
    selectioncategory = get_selection_categories(db)
    print(selectioncategory)
    jsonobj = json.dumps(selectioncategory)
    return jsonobj


@app.route("/getselectioninfo")
def getselectioninfo():
    selectionid = request.args.get("selection_id",None)
    db = get_db()
    selectioninfo = get_selection_by_id(db,selectionid)
    print(selectioninfo)
    jsonselectioninfo = json.dumps(selectioninfo)
    return jsonselectioninfo

@app.route("/coursecontainselections")
def coursecontainselections():
    courseid = request.args.get("course_id",None)
    db = get_db()
    selectioncourse = get_selections_by_course(db,courseid)
    print(selectioncourse)
    jsonselectioncourse = json.dumps(selectioncourse)
    return jsonselectioncourse

if __name__ == "__main__":
    #app.run(host='0.0.0.0', port=80)
    app.run() 