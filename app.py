import os
import requests
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import plotly.graph_objects as go

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variables
API_KEY = os.getenv('OPENWEATHER_API_KEY')

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    language = request.form.get('language', 'en')  # Default to English
    city = request.form.get('city')

    weather = get_weather(city, language)
    return render_template('index.html', weather=weather)

def get_weather(city, lang='en'):
    WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric',
        'lang': lang  # Add language to the request
    }
    response = requests.get(WEATHER_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        return {
            'city': data['name'],
            'temperature': data['main']['temp'],
            'description': data['weather'][0]['description'],
            'icon': data['weather'][0]['icon']
        }
    else:
        return {'error': 'City not found!'}

@app.route('/location_weather')
def location_weather():
    lat = request.args.get('lat')
    lon = request.args.get('lon')

    WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'lat': lat,
        'lon': lon,
        'appid': API_KEY,
        'units': 'metric'
    }

    response = requests.get(WEATHER_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        return jsonify({
            'city': data['name'],
            'temperature': data['main']['temp'],
            'description': data['weather'][0]['description'],
            'humidity': data['main']['humidity'],
            'wind_speed': data['wind']['speed'],
            'icon': data['weather'][0]['icon']
        })
    else:
        return jsonify({
            'error': 'Unable to fetch weather data for your location'
        }), 404

@app.route('/weather_graph')
def weather_graph():
    forecast = [
        {'date': '2024-11-30', 'temperature': 23, 'humidity': 60, 'wind_speed': 12},
        {'date': '2024-12-01', 'temperature': 22, 'humidity': 65, 'wind_speed': 10},
        {'date': '2024-12-02', 'temperature': 21, 'humidity': 70, 'wind_speed': 8},
        # Add more forecast data here
    ]

    fig = create_weather_graph(forecast)
    return fig.to_html()

def create_weather_graph(forecast):
    dates = [entry['date'] for entry in forecast]
    temps = [entry['temperature'] for entry in forecast]
    humidity = [entry['humidity'] for entry in forecast]
    wind_speed = [entry['wind_speed'] for entry in forecast]
    
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=dates, y=temps, mode='lines+markers', name='Temperature'))
    fig.add_trace(go.Scatter(x=dates, y=humidity, mode='lines+markers', name='Humidity'))
    fig.add_trace(go.Scatter(x=dates, y=wind_speed, mode='lines+markers', name='Wind Speed'))

    fig.update_layout(title='Weather Trends', xaxis_title='Date', yaxis_title='Value')
    return fig

@app.route('/weather')
def weather():
    city = request.args.get('city')
    if not city:
        return jsonify({'error': 'City is required', 'status': 'error'}), 400

    unit = request.args.get('unit', 'metric')
    
    try:
        # Get weather data
        weather_response = requests.get(
            "http://api.openweathermap.org/data/2.5/weather",
            params={
                'q': city,
                'appid': API_KEY,
                'units': unit
            }
        )
        
        if weather_response.status_code == 200:
            weather_data = weather_response.json()
            lat, lon = weather_data['coord']['lat'], weather_data['coord']['lon']
            
            # Get air quality data
            air_response = requests.get(
                "http://api.openweathermap.org/data/2.5/air_pollution",
                params={
                    'lat': lat,
                    'lon': lon,
                    'appid': API_KEY
                }
            )
            
            air_data = None
            aqi = None
            components = None
            if air_response.status_code == 200:
                air_data = air_response.json()
                if 'list' in air_data and len(air_data['list']) > 0:
                    aqi = air_data['list'][0]['main']['aqi']
                    components = air_data['list'][0]['components']
                    air_quality = {
                        'aqi': aqi,
                        'level': get_aqi_level(aqi),
                        'components': components
                    }
            
            return jsonify({
                'status': 'success',
                'data': {
                    'city': weather_data['name'],
                    'country': weather_data['sys']['country'],
                    'temperature': weather_data['main']['temp'],
                    'feels_like': weather_data['main']['feels_like'],
                    'description': weather_data['weather'][0]['description'],
                    'humidity': weather_data['main']['humidity'],
                    'wind_speed': weather_data['wind']['speed'],
                    'pressure': weather_data['main']['pressure'],
                    'clouds': weather_data['clouds']['all'],
                    'sunrise': weather_data['sys']['sunrise'],
                    'sunset': weather_data['sys']['sunset'],
                    'icon': weather_data['weather'][0]['icon'],
                    'air_quality': air_quality if air_quality is not None else None
                }
            })
        
        return jsonify({
            'error': 'City not found!',
            'status': 'error'
        }), weather_response.status_code
            
    except Exception as e:
        print(f"Error fetching weather data: {e}")  # Add logging
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

def get_aqi_level(aqi):
    levels = {
        1: 'Good',
        2: 'Fair',
        3: 'Moderate',
        4: 'Poor',
        5: 'Very Poor'
    }
    return levels.get(aqi, 'Unknown')

@app.route('/suggest-cities')
def suggest_cities():
    query = request.args.get('query', '')
    if len(query) < 2:
        return jsonify([])

    try:
        response = requests.get(
            "http://api.openweathermap.org/geo/1.0/direct",
            params={
                'q': query,
                'limit': 5,
                'appid': API_KEY
            }
        )
        
        if response.status_code == 200:
            cities = response.json()
            suggestions = [{
                'name': city['name'],
                'state': city.get('state', ''),
                'country': city['country'],
                'lat': city['lat'],
                'lon': city['lon']
            } for city in cities]
            return jsonify(suggestions)
        
        return jsonify([])

    except Exception as e:
        print(f"Error in suggest-cities: {e}")
        return jsonify([])

if __name__ == "__main__":
    app.run(debug=True)
