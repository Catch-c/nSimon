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
setChangelogBlueprint = Blueprint('setChangelogBlueprint', __name__)




# --[[ Route ]]--
@setChangelogBlueprint.route("/api/setChangelog", methods=["POST"])
def setChangelog():
    username = request.cookies.get("username")
    changelog = request.json.get(
        "changelog"
    )

    if changelog not in ["true", "false"]:
        return "Invalid theme", 400

    result = Database.databaseChangeChangelog(username, changelog)

    if result == 200:
        return "Changelog updated", 200
    else:
        return "Failed to update Changelog Choice", 500