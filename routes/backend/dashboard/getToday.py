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
getTodayBlueprint = Blueprint('getTodayBlueprint', __name__)




# --[[ Route ]]--
@getTodayBlueprint.route("/api/getToday", methods=["POST"])
def getToday():
    cookie = request.cookies.get("adAuthCookie")

    return jsonify(Simon.getCalendarEvents(cookie)), 200
