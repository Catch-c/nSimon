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
getDailyMessagesBlueprint = Blueprint('getDailyMessagesBlueprint', __name__)




# --[[ Route ]]--
@getDailyMessagesBlueprint.route("/api/getDailyMessages", methods=["POST"])
def getMessages():
    cookie = request.cookies.get("adAuthCookie")
    data = request.json
    date = data["date"]

    return jsonify(Simon.getDailyMessages(cookie, date)), 200