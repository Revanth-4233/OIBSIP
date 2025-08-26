from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Weather App</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      text-align: center;
      background: #e3f2fd;
      margin: 0;
      padding: 0;
    }
    .container {
      background: #fff;
      width: 40%;
      height: 800px;
      margin: 120px auto;
      padding: 50px;
      border-radius: 12px;
      box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    h2 {
      margin-bottom: 20px;
      color: #333;
    }
    input {
      width: 90%;
      padding: 30px;
      margin: 20px 0;
      border-radius: 6px;
      border: 1px solid #ccc;
      font-size: 30px;
    }
    button {
      width: 95%;
      padding: 30px;
      margin-top: 25px;
      background: #2196F3;
      color: white;
      border: none;
      border-radius: 6px;
      cursor: pointer;
      font-size: 30px;
    }
    button:hover {
      background: #1976D3;
    }
    .result {
      margin-top: 20px;
      font-size: 30px;
      font-weight: bold;
      color: #444;
      padding: 30px;
      border-radius: 8px;
      background: #f1f8e9;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>🌤 Weather App</h1>
    <form method="POST">
      <input type="text" name="city" placeholder="Enter city name" required>
      <button type="submit">Get Weather</button>
    </form>

    {% if weather %}
      <div class="result">
        Weather in <b>{{ weather.city }}, {{ weather.country }}</b><br>
        🌡 Temperature: {{ weather.temp }}°C<br>
        💧 Humidity: {{ weather.humidity }}%<br>
        🌍 Condition: {{ weather.condition }}
      </div>
    {% endif %}

    {% if error %}
      <div class="result" style="background:#ffebee;color:#c62828;">
        {{ error }}
      </div>
    {% endif %}
  </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def weather_app():
    weather = None
    error = None
    API_KEY = "802e7173ad3a4031fa36fa13497438d2"
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

    if request.method == "POST":
        city = request.form.get("city", "").strip()
        if city:
            try:
                params = {"q": city, "appid": API_KEY, "units": "metric"}
                response = requests.get(BASE_URL, params=params)
                data = response.json()

                if response.status_code == 200:
                    weather = {
                        "city": data["name"],
                        "country": data["sys"]["country"],
                        "temp": data["main"]["temp"],
                        "humidity": data["main"]["humidity"],
                        "condition": data["weather"][0]["description"].title()
                    }
                else:
                    error = data.get("message", "Unable to fetch weather.")
            except Exception as e:
                error = f"Something went wrong: {e}"

    return render_template_string(html_code, weather=weather, error=error)


if __name__ == "__main__":
    app.run(debug=True)
