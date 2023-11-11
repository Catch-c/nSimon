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
showTaskBlueprint = Blueprint('showTaskBlueprint', __name__)




# --[[ Route ]]--
@showTaskBlueprint.route("/classes/<classID>/task/<taskID>", methods=["GET"])
def classesTaskShow(classID, taskID):
    cookie = request.cookies.get("adAuthCookie")

    if not cookie:
        return redirect('/')

    if not Simon.checkCookie(cookie):
        return redirect('/')

    return render_template("classes/classesShowTask.html", VERSION=current_app.config['VERSION'], classID=classID, taskID=taskID)