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
import random, string, time, json
from datetime import datetime





# --[[ Blueprint Setup ]]--
getShareBlueprint = Blueprint('getShareBlueprint', __name__)




# --[[ Route ]]--
@getShareBlueprint.route("/api/getShare", methods=["POST"])
def getShare():

    data = request.json
    code = data["code"]

    return jsonify(Database.databaseGetShareData(code)), 200