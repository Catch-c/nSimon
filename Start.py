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

app = Flask(__name__)
app.secret_key = "your_secret_key_here"


@app.route("/api/getTimetable", methods=["GET"])
def getTimetable():
    cookie = request.args.get("cookie")
    date = request.args.get("date")

    return jsonify(Simon.getTimetable(cookie, date)), 200


@app.route("/api/getDailyMessages", methods=["GET"])
def getMessages():
    cookie = request.args.get("cookie")
    date = request.args.get("date")

    return jsonify(Simon.getDailyMessages(cookie, date)), 200


@app.route("/api/getUserInfo", methods=["GET"])
def getUserInfo():
    cookie = request.args.get("cookie")

    return jsonify(Simon.getUserInfo(cookie)), 200


@app.route("/api/getClasses", methods=["GET"])
def getClasses():
    cookie = request.args.get("cookie")

    return jsonify(Simon.getClasses(cookie)), 200


@app.route("/api/getToday", methods=["GET"])
def getToday():
    cookie = request.args.get("cookie")

    return jsonify(Simon.getToday(cookie)), 200


@app.route("/api/getWeather", methods=["GET"])
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

    requestURL = f"https://api.open-meteo.com/v1/forecast?latitude={LATITUDE}&longitude={LONGITUDE}&hourly=temperature_2m&daily=weathercode,temperature_2m_max,temperature_2m_min,apparent_temperature_max,apparent_temperature_min,sunrise,sunset,uv_index_max,uv_index_clear_sky_max,precipitation_sum,rain_sum,showers_sum,snowfall_sum,precipitation_hours,precipitation_probability_max,windspeed_10m_max,windgusts_10m_max,winddirection_10m_dominant,shortwave_radiation_sum,et0_fao_evapotranspiration&current_weather=true&timezone=Australia%2FSydney&models=best_match"
    response = requests.get(requestURL)
    data = response.json()

    if response.status_code == 200:
        current_temp = data["current_weather"]["temperature"]
        current_time = data["current_weather"]["time"]

        time_part = current_time.split("T")[1]
        hour = int(time_part.split(":")[0])

        next_hour_temp = data["hourly"]["temperature_2m"][hour + 1]
        next_2_hour_temp = data["hourly"]["temperature_2m"][hour + 2]
        next_3_hour_temp = data["hourly"]["temperature_2m"][hour + 3]

        sunrise = data["daily"]["sunrise"][0].split("T")[1]
        sunset = data["daily"]["sunset"][0].split("T")[1]

        return (
            jsonify(
                {
                    "campus": campus,
                    "currentTemp": current_temp,
                    "oneHour": next_hour_temp,
                    "twoHour": next_2_hour_temp,
                    "threeHour": next_3_hour_temp,
                    "sunrise": sunrise,
                    "sunset": sunset,
                    "precipitation": data["daily"]["precipitation_sum"][0],
                }
            ),
            200,
        )
    else:
        jsonify(
            {
                "campus": campus,
                "currentTemp": "??",
                "oneHour": "??",
                "twoHour": "??",
                "threeHour": "??",
                "sunrise": "?:??",
                "sunset": "?:??",
                "precipitation": "???",
            }
        ), 200


@app.route("/api/checkCookie", methods=["GET"])
def checkCookie():
    cookie = request.args.get("cookie")

    if not Simon.checkCookie(cookie):
        return jsonify({"status": False}), 404
    else:
        return jsonify({"status": True}), 200


@app.route("/api/getCookie", methods=["GET"])
def getCookie():
    username = request.args.get("username")
    password = request.args.get("password")
    campus = request.args.get("campus")

    status, cookie = Simon.login(username, password)

    if status == 404:
        return jsonify({"status": 404}), 404
    else:
        return jsonify({"status": 200, "cookie": cookie}), 200


@app.route("/api/getUserProfileInfo", methods=["GET"])
def getUserProfileInfo():
    cookie = request.args.get("cookie")

    GUID = Simon.getUserInfo(cookie)["d"]["guid"]

    profileInfo = Simon.getUserProfileInfo(cookie, GUID)
    if not profileInfo:
        return jsonify({"status": 404}), 404
    else:
        return jsonify({"status": 200, "data": profileInfo}), 200


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    status, cookie = Simon.login(username, password)

    if status == 404:
        flash("This is a message from the backend.")
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
        response.set_cookie("adAuthCookie", cookie)
        response.set_cookie("campus", campus)
        return response


@app.route("/logout")
def logout():
    response = make_response(redirect(url_for("dashboard")))
    response.set_cookie("adAuthCookie", "")
    response.set_cookie("campus", "")

    return response


@app.route("/dashboard")
def dashboard():
    cookie = request.cookies.get("adAuthCookie")
    campus = request.cookies.get("campus")

    if not cookie:
        return redirect(url_for("home"))

    if not campus:
        return redirect(url_for("home"))

    if not Simon.checkCookie(cookie):
        return redirect(url_for("home"))

    return render_template("dashboard.html", cookie=cookie, campus=campus)


@app.route("/profile")
def profile():
    cookie = request.cookies.get("adAuthCookie")
    campus = request.cookies.get("campus")

    if not cookie:
        return redirect(url_for("home"))

    if not campus:
        return redirect(url_for("home"))

    if not Simon.checkCookie(cookie):
        return redirect(url_for("home"))

    return render_template("profile.html", cookie=cookie, campus=campus)


@app.route("/support")
def support():
    cookie = request.cookies.get("adAuthCookie")
    campus = request.cookies.get("campus")

    if not cookie:
        return redirect(url_for("home"))

    if not Simon.checkCookie(cookie):
        return redirect(url_for("home"))

    return render_template("support.html", cookie=cookie, campus=campus)


@app.route("/settings")
def settings():
    cookie = request.cookies.get("adAuthCookie")
    campus = request.cookies.get("campus")

    if not cookie:
        return redirect(url_for("home"))

    if not Simon.checkCookie(cookie):
        return redirect(url_for("home"))

    return render_template("settings.html", cookie=cookie, campus=campus)


@app.route("/")
def home():
    cookie = request.cookies.get("adAuthCookie")
    if cookie:
        return redirect(url_for("dashboard"))
    return render_template("home.html")


if __name__ == "__main__":
    from waitress import serve
    print("STARTED!")
    serve(app, host="0.0.0.0", port=8080)

# if __name__ == "__main__":
#     app.run(debug=True, port=8080)
