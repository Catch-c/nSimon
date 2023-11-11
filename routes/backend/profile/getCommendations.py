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
import VERSION as VERSION





# --[[ Blueprint Setup ]]--
getCommendationsBlueprint = Blueprint('getCommendationsBlueprint', __name__)




# --[[ Route ]]--
@getCommendationsBlueprint.route("/api/getCommendations", methods=["POST"])
def getCommendations():
    cookie = request.cookies.get("adAuthCookie")

    GUID = Simon.getUserInformation(cookie)["d"]["guid"]

    return jsonify(Simon.getCommendations(cookie, GUID)), 200