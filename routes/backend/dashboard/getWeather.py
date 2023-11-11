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
import VERSION as VERSION
import requests





# --[[ Blueprint Setup ]]--
getWeatherBlueprint = Blueprint('getWeatherBlueprint', __name__)




# --[[ Route ]]--
@getWeatherBlueprint.route("/api/getWeather", methods=["POST"])
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

        currentDescription = data["weather"][0]["main"]
        currentIcon = (
            f"http://openweathermap.org/img/wn/{data['weather'][0]['icon']}.png"
        )

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
