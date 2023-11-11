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
getTaskRubricBlueprint = Blueprint('getTaskRubricBlueprint', __name__)




# --[[ Route ]]--
@getTaskRubricBlueprint.route("/api/getTaskRubric", methods=["POST"])
def getTaskRubric():
    cookie = request.cookies.get("adAuthCookie")

    data = request.json
    classID = data["classID"]
    taskID = data["taskID"]

    return jsonify(Simon.getTaskRubric(cookie, classID, taskID)), 200