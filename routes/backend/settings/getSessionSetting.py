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
getSessionSettingBlueprint = Blueprint('getSessionSettingBlueprint', __name__)




# --[[ Route ]]--
@getSessionSettingBlueprint.route("/api/getSessionSetting", methods=["POST"])
def getSession():
    username = request.cookies.get("username")

    session = Database.databaseGetSession(username)
    return session