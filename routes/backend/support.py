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
import requests, json





# --[[ Blueprint Setup ]]--
supportBlueprint = Blueprint('supportBlueprint', __name__)




# --[[ Route ]]--
@supportBlueprint.route("/api/postSupport", methods=["POST"])
def postSupport():
    try:
        requestType = request.form.get("supportTypeSelect")
        requestTitle = request.form.get("supportTitle")
        requestDescription = request.form.get("supportDescription")
        username = request.cookies.get("username")

        webhookURL = "https://discord.com/api/webhooks/1171271021366607893/qmHqgQ18ohmo-SdfktiHVcFcrXUm7ltmvJxOnaeUT4aHV344LkuZpSHT2D52hZfPAMjx"

        if requestType == "suggestion":
            webhookURL = "https://discord.com/api/webhooks/1171271238224707745/DJ4i7XqCoOWazHsePotgIMgMdz1wEJGrVj6WlFVZNwdTxSt6TlY6yr2beBYlGFleKRqx"
        elif requestType == "bug":
            webhookURL = "https://discord.com/api/webhooks/1171271307875340319/GLtBfWOYVfvS8QSPwCEdKzUFiNvhTdQ5ZFoqedY0dPmA1xRzc34-6QVJL2ztBw1mPG8c"
        else:
            webhookURL = "https://discord.com/api/webhooks/1171271021366607893/qmHqgQ18ohmo-SdfktiHVcFcrXUm7ltmvJxOnaeUT4aHV344LkuZpSHT2D52hZfPAMjx"

        embed = {
            "title": "New Support Request",
            "description": "",
            "color": 3551903,
            "fields": [
                {"name": "Title", "value": requestTitle, "inline": False},
                {"name": "Description", "value": requestDescription, "inline": False},
                {"name": "Username", "value": username, "inline": False},
            ],
        }

        message = {"content": "<@&1151349503203491840>", "embeds": [embed]}

        data = json.dumps(message)

        headers = {"Content-Type": "application/json"}

        response = requests.post(webhookURL, data=data, headers=headers)

        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": "Form submission failed"}), 500