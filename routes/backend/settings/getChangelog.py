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
getChangelogBlueprint = Blueprint('getChangelogBlueprint', __name__)




# --[[ Route ]]--
@getChangelogBlueprint.route("/api/getChangelog", methods=["POST"])
def getChangelog():
    username = request.cookies.get("username")

    changelog = Database.databaseGetChangelog(username)
    return changelog