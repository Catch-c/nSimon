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
getResultInfoBlueprint = Blueprint('getResultInfoBlueprint', __name__)




# --[[ Route ]]--
@getResultInfoBlueprint.route("/api/getResultInfo", methods=["POST"])
def getResultInfo():
    cookie = request.cookies.get("adAuthCookie")

    data = request.json
    classID = data["classID"]
    taskID = data["taskID"]

    return jsonify(Simon.getTaskSubmission(cookie, classID, taskID)), 200