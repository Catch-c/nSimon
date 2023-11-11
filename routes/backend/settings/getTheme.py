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
getThemeBlueprint = Blueprint('getThemeBlueprint', __name__)




# --[[ Route ]]--
@getThemeBlueprint.route("/api/getTheme", methods=["POST"])
def getTheme():
    username = request.cookies.get("username")

    theme = Database.databaseGetTheme(username)
    if theme is not None:
        return theme
    else:
        return jsonify({"error": "Theme not found"}, 404)