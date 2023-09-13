from flask import Flask, render_template, request, redirect, make_response, url_for
import Simon as Simon
import datetime, re, requests

def get_weather():
    BASE_URL = 'https://api.open-meteo.com/v1/forecast?latitude=-38.041&longitude=145.349&hourly=temperature_2m&daily=weathercode,temperature_2m_max,temperature_2m_min,apparent_temperature_max,apparent_temperature_min,sunrise,sunset,uv_index_max,uv_index_clear_sky_max,precipitation_sum,rain_sum,showers_sum,snowfall_sum,precipitation_hours,precipitation_probability_max,windspeed_10m_max,windgusts_10m_max,winddirection_10m_dominant,shortwave_radiation_sum,et0_fao_evapotranspiration&current_weather=true&timezone=Australia%2FSydney&models=best_match'
    


    response = requests.get(BASE_URL)
    data = response.json()


    if response.status_code == 200:
        current_temp = data['current_weather']['temperature']
        current_time = data['current_weather']['time']

        time_part = current_time.split('T')[1]
        hour = int(time_part.split(':')[0])

        next_hour_temp = data['hourly']['temperature_2m'][hour+1]
        next_2_hour_temp = data['hourly']['temperature_2m'][hour+2]
        next_3_hour_temp = data['hourly']['temperature_2m'][hour+3]

        sunrise = data['daily']['sunrise'][0].split('T')[1]
        sunset = data['daily']['sunset'][0].split('T')[1]



        return 200, {
            "currentTemp": current_temp,
            "oneHour": next_hour_temp,
            "twoHour": next_2_hour_temp,
            "threeHour": next_3_hour_temp,
            "sunrise": sunrise,
            "sunset": sunset,
            "precipitation": data['daily']['precipitation_sum'][0]
        }


    else:
        return 100, None







app = Flask(__name__)

def convert12Hour(time_str):
    # Parse the 24-hour time string into a datetime object
    dt = datetime.datetime.strptime(time_str, "%H:%M")
    
    # Format the datetime object into a 12-hour format string with AM/PM
    return dt.strftime("%I:%M%p")
app.jinja_env.filters['convert12Hour'] = convert12Hour

def strip_prefix(input_str):
    return input_str.split("_")[-1] if "BER_" in input_str else input_str
app.jinja_env.filters['strip_prefix'] = strip_prefix

def strip_timetable(input_str):
    return input_str.replace("Timetable ", "").strip()
app.jinja_env.filters['strip_timetable'] = strip_timetable

def allow_br_tags_only(input_str):
    # First, replace <br> tags with a placeholder to prevent them from getting removed
    temp_str = input_str.replace('<br>', '[BR]')
    
    # Strip out all other HTML tags
    stripped = re.sub(r'<[^>]+>', '', temp_str)
    
    # Restore the <br> tags
    return stripped.replace('[BR]', '<br>')
app.jinja_env.filters['allow_br_tags_only'] = allow_br_tags_only






@app.route('/')
def home():
    user_id = request.cookies.get('user_id')
    if user_id:
        return redirect(url_for('dashboard'))
    return render_template('home.html')

@app.route('/submit', methods=['POST'])
def submit_id():
    user_id = request.form.get('user_id')
    response = make_response(redirect(url_for('dashboard')))
    response.set_cookie('user_id', user_id)
    return response

@app.route('/dashboard')
def dashboard():
    user_id = request.cookies.get('user_id')
    if not user_id:
        return redirect(url_for('home'))

    timetable = Simon.getTimetable(user_id, datetime.datetime.now().isoformat() + 'Z')
    dailyMessages = Simon.getDailyMessages(user_id, datetime.datetime.now().isoformat() + 'Z')
    userInformation = Simon.getUserInfo(user_id)
    today = Simon.getToday(user_id)
    classesD = Simon.getClasses(user_id)

    classes = timetable["d"]["Periods"]
    dailyMessages = dailyMessages["d"]["SchoolMessages"]
    userInformation = userInformation["d"]
    today = today["d"]["Events"]
    overdueTasks = len(classesD["d"]["OverDueTasksStudent"])
    dueTasks = len(classesD["d"]["DueTasksStudent"])
    resultsTasks = len(classesD["d"]["ResultTasksStudent"])

    status, weather = get_weather()

    if status == 100:
        weather = {
            "currentTemp": 10,
            "oneHour": 11,
            "twoHour": 12,
            "threeHour": 13,
            "sunrise": "05:00",
            "sunset": "20:00",
            "precipitation": 0
        }



    return render_template('dashboard.html', weather=weather, userInformation=userInformation, classes=classes, fullTimetable=timetable, dailyMessages=dailyMessages, today=today, overdueTasks=overdueTasks, dueTasks=dueTasks, resultsTasks=resultsTasks)

# if __name__ == '__main__':
#     app.run(debug=True)

if __name__ == "__main__":
    from waitress import serve
    print("STARTED!")
    serve(app, host="0.0.0.0", port=8080)
