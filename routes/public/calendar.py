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
calendarBlueprint = Blueprint('calendarBlueprint', __name__)




# --[[ Route ]]--
@calendarBlueprint.route('/calendar')
def calendar():

    cookie = request.cookies.get("adAuthCookie")

    if not cookie:
        return redirect('/')

    if not Simon.checkCookie(cookie):
        return redirect('/')

    return render_template("main/calendar.html", VERSION=current_app.config['VERSION'])
