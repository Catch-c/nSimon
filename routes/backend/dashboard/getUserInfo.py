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
getUserInfoBlueprint = Blueprint('getUserInfoBlueprint', __name__)




# --[[ Route ]]--
@getUserInfoBlueprint.route("/api/getUserInfo", methods=["POST"])
def getUserInfo():
    cookie = request.cookies.get("adAuthCookie")

    return jsonify(Simon.getUserInformation(cookie)), 200