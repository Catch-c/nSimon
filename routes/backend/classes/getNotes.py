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
getNotesBlueprint = Blueprint('getNotesBlueprint', __name__)




# --[[ Route ]]--
@getNotesBlueprint.route("/api/getNotes", methods=["POST"])
def getNotes():
    username = request.cookies.get("username")

    cNotes = Database.databaseGetNotes(username)

    if cNotes == {}:
        cNotes = {"classes": {}, "tasks": {}}
        Database.databaseChangeNotes(username, cNotes)

    return jsonify(cNotes), 200
