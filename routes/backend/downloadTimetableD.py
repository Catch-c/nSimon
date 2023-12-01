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
    send_from_directory
)
import Database as Database
import Simon as Simon





# --[[ Blueprint Setup ]]--
downloadTimetableDBlueprint = Blueprint('downloadTimetableDBlueprint', __name__)


@downloadTimetableDBlueprint.route('/d/<filename>')
def downloadTimetableD(filename):
    return send_from_directory('static/timetables', filename)