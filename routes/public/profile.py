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
profileBlueprint = Blueprint('profileBlueprint', __name__)




# --[[ Route ]]--
@profileBlueprint.route("/profile")
def profile():
    cookie = request.cookies.get("adAuthCookie")

    if not cookie:
        return redirect('/')

    if not Simon.checkCookie(cookie):
        return redirect('/')

    return render_template("main/profile.html", VERSION=VERSION.VERSION)
