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
import Timetable as Timetable
import random, string, time, json
from datetime import datetime, timedelta
import pytz


# --[[ Blueprint Setup ]]--
downloadTimetableBlueprint = Blueprint("downloadTimetableBlueprint", __name__)


# --[[ Route ]]--
@downloadTimetableBlueprint.route("/api/downloadTimetable", methods=["POST"])
def downloadTimetable():
    username = request.cookies.get("username")
    cookie = request.cookies.get("adAuthCookie")
    campus = request.cookies.get("campus")

    campusCode = None

    if campus == "Berwick":
        campusCode = "BER"
    elif campus == "Beaconsfield":
        campusCode = "BEA"
    elif campus == "Officer":
        campusCode = "OFF"

    local_timezone = pytz.timezone('Australia/Sydney')  # AEDT timezone

    today = datetime.now(local_timezone)
    next_monday = today + timedelta(days=(7 - today.weekday()))

    gmt_timezone = pytz.timezone('GMT')

    weekdays = []
    current_date = next_monday

    while len(weekdays) < 10:
        if current_date.weekday() < 5:
            current_date_gmt = current_date.astimezone(gmt_timezone)
            weekdays.append(current_date_gmt.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))

        current_date += timedelta(days=1)

    timetable = {}

    count = 1
    for date in weekdays:
        timetable[str(count)] = Simon.getTimetable(cookie, date, campusCode)
        count += 1

    for i in range(1, 11):
        if not timetable[str(i)]['d']['Periods']:
            return jsonify({"Error": 100, "data": timetable})

    url = Timetable.create(
        username,
        timetable
    )
    return jsonify({"Success": url})
