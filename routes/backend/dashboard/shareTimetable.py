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
import random, string, time, json
from datetime import datetime





# --[[ Blueprint Setup ]]--
shareTimetableBlueprint = Blueprint('shareTimetableBlueprint', __name__)




# --[[ Route ]]--
@shareTimetableBlueprint.route("/api/shareTimetable", methods=["POST"])
def shareTimetable():
    username = request.cookies.get("username")
    data = request.json
    timetable = data["timetableData"]

    dtObject = datetime.utcfromtimestamp(int(time.time()))
    DDMMYYYY = dtObject.strftime('%d%m%Y')

    currentSharedTimetables = Database.databaseGetSharedTimetables(username)

    if DDMMYYYY in currentSharedTimetables:
        return jsonify({"error": "Already Created", "code": currentSharedTimetables[DDMMYYYY]}), 200

    characters = string.ascii_letters + string.digits
    random_code = ''.join(random.choice(characters) for _ in range(9))



    shareD = {
        "owner": username,
        "date": DDMMYYYY,
        "data": timetable
    }

    Database.databaseCreateShare(random_code, shareD)

    currentSharedTimetables[DDMMYYYY] = random_code
    Database.databaseChangeSharedTimetables(username, currentSharedTimetables)


    return jsonify({"code": random_code}), 200