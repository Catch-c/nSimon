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
getTimetableBlueprint = Blueprint('getTimetableBlueprint', __name__)




# --[[ Route ]]--
@getTimetableBlueprint.route("/api/getTimetable", methods=["POST"])
def getTimetable():
    cookie = request.cookies.get("adAuthCookie")
    data = request.json
    date = data["date"]

    return jsonify(Simon.getTimetable(cookie, date)), 200