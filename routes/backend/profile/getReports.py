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
getReportsBlueprint = Blueprint('getReportsBlueprint', __name__)




# --[[ Route ]]--
@getReportsBlueprint.route("/api/getReports", methods=["POST"])
def getReports():
    cookie = request.cookies.get("adAuthCookie")

    GUID = Simon.getUserInformation(cookie)["d"]["guid"]

    return jsonify(Simon.getAssessmentReports(cookie, GUID)), 200