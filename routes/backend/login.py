# --[[ Imports ]]--
from flask import (
    Flask,
    request,
    jsonify,
    redirect,
    render_template,
    url_for,
    make_response,
    flash,
    Blueprint,
    current_app,
)
import Database as Database
import Simon as Simon





# --[[ Blueprint Setup ]]--
loginBlueprint = Blueprint('loginBlueprint', __name__)




# --[[ Route ]]--
@loginBlueprint.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    rememberme = request.form.get("rememberme")

    result = Database.databaseCheckUser(username, password)

    if result == 404:
        status, cookie = Simon.login(username, password)

        if status == 404:
            flash("Incorrect password")
            return redirect('/')

        Database.databaseAddUser(username, password, cookie)
    elif result == 403:
        flash("Incorrect password")
        return redirect('/')
    else:
        _, cookie = result

    timetableData = Simon.getTimetable(cookie, "2023-08-09T21:02:04.085Z", None)
    campusCode = timetableData["DefaultTimeTableGroup"]

    if campusCode == "BER":
        campus = "Berwick"
    elif campusCode == "BEA":
        campus = "Beaconsfield"
    elif campusCode == "OFF":
        campus = "Officer"
    else:
        campus = "Beaconsfield"

    response = make_response(redirect('/dashboard'))

    if rememberme == "on":
        response.set_cookie("adAuthCookie", cookie, max_age=7776000)
        response.set_cookie("username", username, max_age=7776000)
        response.set_cookie("campus", campus, max_age=7776000)
        response.set_cookie("loginVer", "1.1", max_age=7776000)
    else:
        response.set_cookie("adAuthCookie", cookie)
        response.set_cookie("username", username)
        response.set_cookie("campus", campus)
        response.set_cookie("loginVer", "1.1")

    return response
