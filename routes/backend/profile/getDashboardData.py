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
getDashboardDataBlueprint = Blueprint('getDashboardDataBlueprint', __name__)




# --[[ Route ]]--
@getDashboardDataBlueprint.route("/api/getDashboardData", methods=["POST"])
def getDashboardData():
    cookie = request.cookies.get("adAuthCookie")

    GUID = Simon.getUserInformation(cookie)["d"]["guid"]

    return jsonify(Simon.getDashboardData(cookie, GUID)), 200