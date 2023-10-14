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
)
import Simon as Simon
import requests
import configparser

# --[[Import Config Values]]--
config = configparser.ConfigParser()
config.read('config.ini')
flask_secret = config.get('Flask', 'flask.secret')

# --[[ Flask Setup ]]--
app = Flask(__name__)
app.secret_key = flask_secret
VERSION = "1.2.10"






# --[[ API Routes ]]--
#       --[[ getTimetable () ]]--
@app.route("/api/getTimetable", methods=["POST"])
def getTimetable():
    cookie = request.cookies.get("adAuthCookie")
    data = request.json
    date = data['date']

    return jsonify(Simon.getTimetable(cookie, date)), 200

#       --[[ getCalendar () ]]--
@app.route("/api/getCalendar", methods=["POST"])
def getCalendar():
    cookie = request.cookies.get("adAuthCookie")
    data = request.json
    date = data['date']


    return jsonify(Simon.getCalendar(cookie, f"{date}T14:00:00.000Z")), 200


#       --[[ getDailyMessages () ]]--
@app.route("/api/getDailyMessages", methods=["POST"])
def getMessages():
    cookie = request.cookies.get("adAuthCookie")
    data = request.json
    date = data['date']

    return jsonify(Simon.getDailyMessages(cookie, date)), 200


#       --[[ getUserInfo () ]]--
@app.route("/api/getUserInfo", methods=["POST"])
def getUserInfo():
    cookie = request.cookies.get("adAuthCookie")

    return jsonify(Simon.getUserInformation(cookie)), 200


#       --[[ getClasses () ]]--
@app.route("/api/getClasses", methods=["POST"])
def getClasses():
    cookie = request.cookies.get("adAuthCookie")

    return jsonify(Simon.getClassResources(cookie)), 200


#       --[[ getClassTasks () ]]--
@app.route("/api/getClassTasks", methods=["POST"])
def getClassTasks():
    cookie = request.cookies.get("adAuthCookie")

    data = request.json
    classID = data['classID']

    return jsonify(Simon.getClassTasks(cookie, classID)), 200


#       --[[ getToday () ]]--
@app.route("/api/getToday", methods=["POST"])
def getToday():
    cookie = request.cookies.get("adAuthCookie")

    return jsonify(Simon.getCalendarEvents(cookie)), 200


#       --[[ getWeather () ]]--
@app.route("/api/getWeather", methods=["POST"])
def getWeather():
    campus = request.cookies.get("campus")
    LATITUDE = -38.069780
    LONGITUDE = 145.336950
    match campus:
        case "Berwick":
            LATITUDE = -38.069780
            LONGITUDE = 145.336950
        case "Beaconsfield":
            LATITUDE = -38.051690
            LONGITUDE = 145.373290
        case "Officer":
            LATITUDE = -38.062630
            LONGITUDE = 145.431780

    requestURL = f"https://api.openweathermap.org/data/2.5/weather?lat={LATITUDE}&lon={LONGITUDE}&units=metric&appid=2c6e63b60282458a0d113423de04dc8d"
    response = requests.get(requestURL)
    data = response.json()

    if response.status_code == 200:

        currentTemperature = data["main"]["temp"]
        currentFeelsLikeTemperature = data["main"]["feels_like"]
        mininumTemperature = data["main"]["temp_min"]
        maximumTemperature = data["main"]["temp_max"]

        currentDescription = data['weather'][0]['main']
        currentIcon = f"http://openweathermap.org/img/wn/{data['weather'][0]['icon']}.png"


        return (
            jsonify(
                {
                    "campus": campus,
                    "currentTemperature": currentTemperature,
                    "currentFeelsLikeTemperature": currentFeelsLikeTemperature,
                    "mininumTemperature": mininumTemperature,
                    "maximumTemperature": maximumTemperature,
                    "currentDescription": currentDescription,
                    "currentIcon": currentIcon,
                }
            ),
            200,
        )
    else:
        jsonify(
            {
                "campus": campus,
                "currentTemperature": "??",
                "currentFeelsLikeTemperature": "??",
                "mininumTemperature": "??",
                "maximumTemperature": "??",
                "currentDescription": "??",
                "currentIcon": "https://openweathermap.org/img/wn/01d.png",
            }
        ), 200


#       --[[ checkCookie () ]]--
@app.route("/api/checkCookie", methods=["POST"])
def checkCookie():
    cookie = request.args.get("cookie")

    if not Simon.checkCookie(cookie):
        return jsonify({"status": False}), 404
    else:
        return jsonify({"status": True}), 200


#       --[[ getCookie () ]]--
@app.route("/api/getCookie", methods=["POST"])
def getCookie():
    username = request.args.get("username")
    password = request.args.get("password")
    campus = request.args.get("campus")

    status, cookie = Simon.login(username, password)

    if status == 404:
        return jsonify({"status": 404}), 404
    else:
        return jsonify({"status": 200, "cookie": cookie}), 200


#       --[[ getUserProfileInfo () ]]--
@app.route("/api/getDashboardData", methods=["POST"])
def getDashboardData():
    cookie = request.cookies.get("adAuthCookie")

    GUID = Simon.getUserInformation(cookie)["d"]["guid"]

    return jsonify(Simon.getDashboardData(cookie, GUID)), 200


#       --[[ getStudentProfile () ]]--
@app.route("/api/getStudentProfile", methods=["POST"])
def getStudentProfile():
    cookie = request.cookies.get("adAuthCookie")

    return jsonify(Simon.getStudentProfile(cookie)), 200


#       --[[ getUserProfileInfo () ]]--
@app.route("/api/getStudentProfileDetails", methods=["POST"])
def getStudentProfileDetails():
    cookie = request.cookies.get("adAuthCookie")

    return jsonify(Simon.getStudentProfileDetails(cookie)), 200

#       --[[ getUserProfileInfo () ]]--
@app.route("/api/getStudentProfileBehaviouralHistory", methods=["POST"])
def getStudentProfileBehaviouralHistory():
    cookie = request.cookies.get("adAuthCookie")

    return jsonify(Simon.getStudentProfileBehaviouralHistory(cookie)), 200



#       --[[ login () ]]--
@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    rememberme = request.form.get("rememberme")

    status, cookie = Simon.login(username, password)

    if status != 200:
        flash(status)
        return redirect(url_for("home"))
    else:

        # GETTING CAMPUS
        timetableData = Simon.getTimetable(cookie, "2023-08-09T21:02:04.085Z")
        campusCode = timetableData["d"]["DefaultTimeTableGroup"]

        if campusCode == "BER":
            campus = "Berwick"
        elif campusCode == "BEA":
            campus = "Beaconsfield"
        elif campusCode == "OFF":
            campus = "Officer"
        else:
            campus = "Beaconsfield"

        response = make_response(redirect(url_for("dashboard")))

        if rememberme == "on":
            response.set_cookie("adAuthCookie", cookie, max_age=7776000)
            response.set_cookie("campus", campus, max_age=7776000)
        else:
            response.set_cookie("adAuthCookie", cookie)
            response.set_cookie("campus", campus)

        return response






# --[[ Frontend Routes ]]--
#       --[[ /logout ]]--
@app.route("/logout")
def logout():
    response = make_response(redirect(url_for("dashboard")))
    response.set_cookie("adAuthCookie", "", max_age=7776000)
    response.set_cookie("campus", "", max_age=7776000)
    return response

#       --[[ /dashboard ]]--
@app.route("/dashboard")
def dashboard():
    cookie = request.cookies.get("adAuthCookie")

    if not cookie:
        return redirect(url_for("home"))

    if not Simon.checkCookie(cookie):
        return redirect(url_for("home"))

    return render_template("dashboard.html", VERSION=VERSION)

#       --[[ /profile ]]--
@app.route("/profile")
def profile():
    cookie = request.cookies.get("adAuthCookie")

    if not cookie:
        return redirect(url_for("home"))

    if not Simon.checkCookie(cookie):
        return redirect(url_for("home"))

    return render_template("profile.html", VERSION=VERSION)

#       --[[ /support ]]--
@app.route("/support")
def support():
    cookie = request.cookies.get("adAuthCookie")

    if not cookie:
        return redirect(url_for("home"))

    if not Simon.checkCookie(cookie):
        return redirect(url_for("home"))

    return render_template("support.html", VERSION=VERSION)

#       --[[ /settings ]]--
@app.route("/settings")
def settings():
    cookie = request.cookies.get("adAuthCookie")

    if not cookie:
        return redirect(url_for("home"))

    if not Simon.checkCookie(cookie):
        return redirect(url_for("home"))

    return render_template("settings.html", VERSION=VERSION)

#       --[[ / ]]--
@app.route("/")
def home():
    cookie = request.cookies.get("adAuthCookie")
    if cookie:
        return redirect(url_for("dashboard"))
    return render_template("home.html", VERSION=VERSION)

#       --[[ /calendar ]]--
@app.route("/calendar")
def calendar():
    cookie = request.cookies.get("adAuthCookie")

    if not cookie:
        return redirect(url_for("home"))

    if not Simon.checkCookie(cookie):
        return redirect(url_for("home"))

    return render_template("calendar.html", VERSION=VERSION)

#       --[[ /classes ]]--
@app.route("/classes")
def classes():
    cookie = request.cookies.get("adAuthCookie")

    if not cookie:
        return redirect(url_for("home"))

    if not Simon.checkCookie(cookie):
        return redirect(url_for("home"))

    return render_template("classes.html", VERSION=VERSION)
@app.route('/classes/<classID>', methods=['GET'])
def classesShow(classID):
    cookie = request.cookies.get("adAuthCookie")

    if not cookie:
        return redirect(url_for("home"))

    if not Simon.checkCookie(cookie):
        return redirect(url_for("home"))

    return render_template("classesShow.html", VERSION=VERSION, classID=classID)







# --[[ Start ]]--
#       --[[ PRODUCTION ]]--
if __name__ == "__main__":
    from waitress import serve
    print("STARTED!")
    serve(app, host="0.0.0.0", port=8080)

#       --[[ TESTING ]]--
# if __name__ == "__main__":
#     app.run(debug=True, port=8080)
