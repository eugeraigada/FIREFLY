import csv
from flask import Flask, render_template, request
import requests
from io import StringIO

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = {}
    fire_risk = ""
    calculated_risk_score = 0

    if request.method == 'POST':
        location = request.form['location']
        csv_data = fetch_weather(location)
        weather_data = parse_csv_to_dict(csv_data)
        fire_risk, calculated_risk_score = calculate_fire_risk(weather_data)

    return render_template('index.html', weather_data=weather_data, fire_risk=fire_risk, calculated_risk_score=calculated_risk_score)

def fetch_weather(location):
    url = "https://visual-crossing-weather.p.rapidapi.com/history"
    querystring = {
        "startDateTime": "2019-01-01T00:00:00",
        "aggregateHours": "24",
        "location": location,
        "endDateTime": "2019-01-03T00:00:00",
        "unitGroup": "us",
        "dayStartTime": "8:00:00",
        "contentType": "csv",
        "dayEndTime": "17:00:00",
        "shortColumnNames": "0"
    }

    headers = {
        "X-RapidAPI-Key": "e5f1f8822cmsh0f514b88eb89b7cp1d8a1ejsnb7906db17b24",
        "X-RapidAPI-Host": "visual-crossing-weather.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code != 200:
        return f"Error: {response.status_code}\n{response.text}"

    return response.text

def parse_csv_to_dict(csv_data):
    reader = csv.DictReader(StringIO(csv_data))
    return [row for row in reader][0]

def calculate_fire_risk(weather_data):
    # Map the fields from weather_data to the variables in the equation
    AvgSurfaceTemp = float(weather_data.get('Temperature', 0))
    AvgWindSpeed = float(weather_data.get('Wind Speed', 0))
    AvgAirTemp = float(weather_data.get('Temperature', 0))
    AvgHumidity = float(weather_data.get('Relative Humidity', 0))
    MinSurfaceTemp = float(weather_data.get('Minimum Temperature', 0))
    MinAirTemp = float(weather_data.get('Minimum Temperature', 0))
    MaxSurfaceTemp = float(weather_data.get('Maximum Temperature', 0))
    MaxAirTemp = float(weather_data.get('Maximum Temperature', 0))
    MaxWindSpeed = float(weather_data.get('Wind Gust', 0))
    MinHumidity = float(weather_data.get('Relative Humidity', 0))
    Precipitation = float(weather_data.get('Precipitation', 0))

    risk_score = (8 * AvgSurfaceTemp + 7 * AvgWindSpeed + 8 * AvgAirTemp - 7 * AvgHumidity +
                  6 * MinSurfaceTemp + 6 * MinAirTemp + 9 * MaxSurfaceTemp + 9 * MaxAirTemp +
                  10 * MaxWindSpeed - 6 * MinHumidity - 10 * Precipitation)
    normalized_risk_score = min(max(int((risk_score / 300) * 100), 0), 100)  # Assuming 300 is the maximum possible risk score

    if normalized_risk_score > 75:
        return "High", normalized_risk_score
    elif normalized_risk_score > 50:
        return "Medium", normalized_risk_score
    else:
        return "Low", normalized_risk_score

if __name__ == '__main__':
    app.run(debug=True)

