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
setThemeBlueprint = Blueprint('setThemeBlueprint', __name__)




# --[[ Route ]]--
@setThemeBlueprint.route("/api/setTheme", methods=["POST"])
def setTheme():
    username = request.cookies.get("username")
    theme = request.json.get(
        "theme"
    )
    if theme not in ["dark", "light", "blue"]:
        return "Invalid theme", 400

    result = Database.databaseChangeTheme(username, theme)

    if result == 200:
        return "Theme updated", 200
    else:
        return "Failed to update theme", 500