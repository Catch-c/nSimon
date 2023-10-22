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
import Database as Database
import requests
import configparser
import logging

# LOGS
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --[[Import Config Values]]--
config = configparser.ConfigParser()
config.read('config.ini')
flask_secret = config.get('Flask', 'secret')

# --[[ Flask Setup ]]--
app = Flask(__name__)
app.secret_key = flask_secret
VERSION = "1.3.4"


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
    


#       --[[ getStudentProfileImage () ]]--
@app.route("/api/getStudentProfileImage", methods=["POST"])
def getStudentProfileImage():
    cookie = request.cookies.get("adAuthCookie")
    username = request.cookies.get("username")

    image_data = Database.databaseCheckImage(username)

    if image_data is None:
        # If the image is not found in the database, add it
        image_data = Database.databaseAddImage(username, cookie)

    if image_data is not None:
        # If image data exists, return it as an image response
        return image_data, 200, {"Content-Type": "image/jpeg"}  # Adjust the content type as needed
    else:
        # If no image data is available, return a placeholder image or an error response
        return "Image not found", 404
    

#       --[[ getTheme () ]]--
@app.route("/api/getTheme", methods=["POST"])
def getTheme():
    username = request.cookies.get("username")

    theme = Database.databaseGetTheme(username)
    if theme is not None:
        return jsonify({"theme": theme})  # Return the theme as JSON response
    else:
        return jsonify({"error": "Theme not found"}, 404)  # Return an error response

#       --[[ setTheme () ]]--
@app.route("/api/setTheme", methods=["POST"])
def setTheme():
    username = request.cookies.get("username")
    theme = request.json.get("theme")  # Assuming the theme is passed in the request JSON

    if theme not in ["dark", "light", "blue", "tiktok"]:
        return "Invalid theme", 400  # Return a bad request response for invalid theme

    result = Database.databaseChangeTheme(username, theme)

    if result == 200:
        return "Theme updated", 200
    else:
        return "Failed to update theme", 500
    
#       --[[ getMusic () ]]--
@app.route("/api/getMusic", methods=["POST"])
def getMusic():
    username = request.cookies.get("username")

    music = Database.databaseGetMusic(username)
    return music

#       --[[ setMusic () ]]--
@app.route("/api/setMusic", methods=["POST"])
def setMusic():
    username = request.cookies.get("username")
    music = request.json.get("music")  # Assuming the theme is passed in the request JSON

    if music not in ["yes", "no"]:
        return "Invalid theme", 400  # Return a bad request response for invalid theme

    result = Database.databaseChangeMusic(username, music)

    if result == 200:
        return "Music updated", 200
    else:
        return "Failed to update Music Choice", 500
    




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

    result = Database.databaseCheckUser(username, password)

    if result == 404:
    # User doesn't exist in the database, so attempt to login using Simon
        status, cookie = Simon.login(username, password)

        if status == 404:
        # Simon.login also failed, show a flash message and redirect to the login page
            flash('Incorrect password')
            return redirect(url_for("home"))

    # If Simon.login was successful, add the user to the database
        Database.databaseAddUser(username, password, cookie)
    elif result == 403:
    # The password is incorrect in the database, so show a flash message and redirect to the login page
        flash('Incorrect password')
        return redirect(url_for("home"))
    else:
    # User exists in the database
        _, cookie = result

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
        response.set_cookie("username", username, max_age=7776000)
        response.set_cookie("campus", campus, max_age=7776000)
    else:
        response.set_cookie("adAuthCookie", cookie)
        response.set_cookie("username", username)
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
    logger.info("nSimon Started!")
    serve(app, host="0.0.0.0", port=8080)

#       --[[ TESTING ]]--
# if __name__ == "__main__":
#     app.run(debug=True, port=8080)
