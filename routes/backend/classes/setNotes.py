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
setNotesBlueprint = Blueprint("setNotesBlueprint", __name__)


# --[[ Route ]]--
@setNotesBlueprint.route("/api/setNotes", methods=["POST"])
def setNotes():
    username = request.cookies.get("username")
    noteType = request.json.get("noteType")
    typeID = request.json.get("typeID")
    note = request.json.get("note")



    cNotes = Database.databaseGetNotes(username)

    if cNotes == {}:
        cNotes = {"classes": {}, "tasks": {}}

    cNotes[noteType][typeID] = note



    result = Database.databaseChangeNotes(username, cNotes)


    if result == 200:
        return "Note updated", 200
    else:
        return "Failed to update note", 500
