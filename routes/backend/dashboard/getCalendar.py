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
getCalendarBlueprint = Blueprint('getCalendarBlueprint', __name__)




# --[[ Route ]]--
@getCalendarBlueprint.route("/api/getCalendar", methods=["POST"])
def getCalendar():
    cookie = request.cookies.get("adAuthCookie")
    data = request.json
    date = data["date"]

    return jsonify(Simon.getCalendar(cookie, f"{date}T14:00:00.000Z")), 200