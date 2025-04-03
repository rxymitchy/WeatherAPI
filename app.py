from flask import Flask, render_template, request, redirect, url_for
import requests
import os

app = Flask(__name__)

# OpenWeatherMap API configuration
API_KEY = os.getenv('OWM_API_KEY', 'YOUR_API_KEY_HERE')
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_weather', methods=['POST'])
def get_weather():
    city = request.form.get('city')
    if not city:
        return redirect(url_for('error', code=400, message="City cannot be empty"))
    
    try:
        params = {
            'q': city,
            'appid': API_KEY,
            'units': 'metric'
        }
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        weather_data = response.json()
        
        return render_template('results.html', 
                             city=city,
                             temp=weather_data['main']['temp'],
                             description=weather_data['weather'][0]['description'],
                             icon=weather_data['weather'][0]['icon'],
                             humidity=weather_data['main']['humidity'],
                             wind=weather_data['wind']['speed'])
    except requests.exceptions.RequestException as e:
        return redirect(url_for('error', code=500, message=str(e)))

@app.route('/error')
def error():
    error_code = request.args.get('code', 500)
    error_message = request.args.get('message', 'An unexpected error occurred')
    return render_template('error.html', 
                         error_code=error_code,
                         error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)