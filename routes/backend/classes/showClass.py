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
showClassBlueprint = Blueprint('showClassBlueprint', __name__)




# --[[ Route ]]--
@showClassBlueprint.route("/classes/<classID>", methods=["GET"])
def classesShow(classID):
    cookie = request.cookies.get("adAuthCookie")

    if not cookie:
        return redirect('/')

    if not Simon.checkCookie(cookie):
        return redirect('/')

    return render_template("classes/classesShow.html", VERSION=VERSION.VERSION, classID=classID)
