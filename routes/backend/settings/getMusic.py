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
getMusicBlueprint = Blueprint('getMusicBlueprint', __name__)




# --[[ Route ]]--
@getMusicBlueprint.route("/api/getMusic", methods=["POST"])
def getMusic():
    username = request.cookies.get("username")

    music = Database.databaseGetMusic(username)
    return music