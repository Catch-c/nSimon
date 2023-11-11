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
logoutBlueprint = Blueprint('logoutBlueprint', __name__)




# --[[ Route ]]--
@logoutBlueprint.route("/logout")
def logout():
    response = make_response(redirect('/'))
    response.set_cookie("adAuthCookie", "", max_age=7776000)
    response.set_cookie("campus", "", max_age=7776000)
    return response