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
indexBlueprint = Blueprint('indexBlueprint', __name__)




# --[[ Route ]]--
@indexBlueprint.route('/')
def index():

    cookie = request.cookies.get("adAuthCookie")
    if cookie:
        return redirect('/dashboard')

    return render_template('main/index.html')
