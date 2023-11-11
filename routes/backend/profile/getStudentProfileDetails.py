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
getStudentProfileDetailsBlueprint = Blueprint('getStudentProfileDetailsBlueprint', __name__)




# --[[ Route ]]--
@getStudentProfileDetailsBlueprint.route("/api/getStudentProfileDetails", methods=["POST"])
def getStudentProfileDetails():
    cookie = request.cookies.get("adAuthCookie")

    return jsonify(Simon.getStudentProfileDetails(cookie)), 200