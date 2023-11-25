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
viewShareBlueprint = Blueprint('viewShareBlueprint', __name__)




# --[[ Route ]]--
@viewShareBlueprint.route('/s/<code>')
def viewShare(code):


    cookie = request.cookies.get("adAuthCookie")
    if cookie:
        redirect_url = f'/dashboard?share={code}'
        return redirect(redirect_url)

    redirect_url = f'/?share={code}'
    return redirect(redirect_url)