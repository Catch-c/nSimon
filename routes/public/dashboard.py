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
dashboardBlueprint = Blueprint('dashboardBlueprint', __name__)




# --[[ Route ]]--
@dashboardBlueprint.route('/dashboard')
def dashboard():

    cookie = request.cookies.get("adAuthCookie")

    username = request.cookies.get("username")
    if Database.databaseFindUser(username) == 404:
        return redirect('/logout')


    if not cookie:
        return redirect('/')

    if not Simon.checkCookie(cookie):
        return redirect('/')

    return render_template("main/dashboard.html")
