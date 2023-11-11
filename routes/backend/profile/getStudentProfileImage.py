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
getStudentProfileImageBlueprint = Blueprint('getStudentProfileImageBlueprint', __name__)




# --[[ Route ]]--
@getStudentProfileImageBlueprint.route("/api/getStudentProfileImage", methods=["POST"])
def getStudentProfileImage():
    cookie = request.cookies.get("adAuthCookie")
    username = request.cookies.get("username")

    image_data = Database.databaseCheckImage(username)

    if image_data is None:
        image_data = Database.databaseAddImage(username, cookie)

    if image_data is not None:
        return (
            image_data,
            200,
            {"Content-Type": "image/jpeg"},
        ) 
    else:
        return "Image not found", 404