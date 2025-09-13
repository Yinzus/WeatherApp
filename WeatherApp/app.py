from flask import Flask, render_template, request, jsonify
import requests
import os
from datetime import datetime, timezone

app = Flask(__name__)

# Uses Open-Meteo (no key required) as default
OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"

@app.get("/")
def index():
    return render_template("index.html")

@app.get("/api/weather")
def api_weather():
    lat = request.args.get("lat")
    lon = request.args.get("lon")
    city = request.args.get("city")

    try:
        if city and (not lat or not lon):
            # Simple geocoding via Open-Meteo geocoding
            geocode = requests.get("https://geocoding-api.open-meteo.com/v1/search", params={"name": city, "count": 1, "language": "en"}).json()
            if not geocode.get("results"):
                return jsonify({"error": "city not found"}), 404
            lat = geocode["results"][0]["latitude"]
            lon = geocode["results"][0]["longitude"]

        if not lat or not lon:
            return jsonify({"error": "lat/lon or city required"}), 400

        params = {
            "latitude": lat,
            "longitude": lon,
            "current_weather": True,
            "hourly": "temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,cloud_cover,wind_speed_10m",
            "forecast_days": 5
        }
        w = requests.get(OPEN_METEO_URL, params=params).json()
        return jsonify(w)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)