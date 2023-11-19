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
privacyBlueprint = Blueprint('privacyBlueprint', __name__)




# --[[ Route ]]--
@privacyBlueprint.route('/privacy')
def privacy():



    return render_template('main/privacy.html')
