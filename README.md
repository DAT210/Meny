# Menu &middot; [![Build Status](https://img.shields.io/travis/npm/npm/latest.svg?style=flat-square)](https://travis-ci.org/npm/npm) [![npm](https://img.shields.io/npm/v/npm.svg?style=flat-square)](https://www.npmjs.com/package/npm) [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com) [![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](https://github.com/your/your-project/blob/master/LICENSE)
> Everything related to the menu of the restaurant.

Developed by Group 4 along with Internal Systems and Food Preparation.
Links to the other repositories:
https://github.com/DAT210/Food-Preparation
https://github.com/DAT210/Internal-Systems

## Running the Menu app 
First clone the repository.

In order for the menu page to work on your system, you need to set up the menu database. 
We have provided a initial script called init_menu_db.sql. This file is located in /Menu/src/db/ folder.
Link to the db folder: https://github.com/DAT210/Menu/tree/master/src/db

Afterwards you need to edit the app.py section: "#Change this the INFORMATION FOR YOUR DATABASE ACCESS OK" on lines between 11-17 in the src/app.py file. 
Edit the database information to match your sql settings, most importantly change "password": "INSERTPASSWORDHERE" to match your sql password.
```
# CHANGE THIS INFORMATION FOR YOUR DATABASE ACCESS OK

user_info = {

    "username": "root",

    "password": "INSERTPASSWORDHERE",

    "database": "menu",

    "hostname": "localhost"

}
```
Since this page doesn't support docker, you also need to make sure that you have imported the needed packages. You can find these on lines 1-5. Mostly its just the flask and mysql.connector packages that needs to be installed on your python intepreter.

Once all this is done you can go to the src folder and run the app.py to start the menu server.
The ip address set for the menu page is http://localhost:5000/ , alternatively http://127.0.0.1:5000/ .

## Developing

### Built With
The menu webpage is built with the Flask framework in Python, HTML-templating with Jinja and JavaScript/jQuery for functionality. It also uses Bootstrap and CSS for styling.

### Prerequisites
Since this page dosen't support docker, you need to install Python, Mysql and MySQL server. 


