---

# Weather Application

A Flask-based web application that fetches weather data using the OpenWeather API. It allows users to search for the weather of a city, view weather trends through a graphical representation, and get air quality data.

## Features

- **Weather Search**: Fetch weather details such as temperature, humidity, wind speed, and description for any city.
- **Location-based Weather**: Get weather data based on your geographical coordinates.
- **Weather Graphs**: Display weather trends (temperature, humidity, wind speed) over several days.
- **Air Quality**: Access air quality data, including AQI and pollutants in the air for a given location.
- **City Suggestions**: Get suggestions for city names based on partial input.

## Technologies Used

- **Flask**: A micro web framework for Python.
- **OpenWeather API**: Provides real-time weather data.
- **Plotly**: A graphing library for creating interactive plots.
- **HTML, CSS, JavaScript**: For building the user interface.
- **Python-dotenv**: For loading environment variables.

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/raj-saurv-sc/weather-app.git
   cd weather-app
   ```

2. **Create a virtual environment**:

   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - On Windows:

     ```bash
     venv\Scripts\activate
     ```

   - On macOS/Linux:

     ```bash
     source venv/bin/activate
     ```

4. **Install the required dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables**:

   - Create a `.env` file in the root directory of your project and add your OpenWeather API key:

     ```
     OPENWEATHER_API_KEY=your_api_key_here
     ```

   - You can get your API key by signing up at [OpenWeather](https://openweathermap.org/api).

## Usage

1. Run the application:

   ```bash
   python app.py
   ```

2. Open your browser and go to `http://127.0.0.1:5000/`.

3. Use the app to:
   - Enter a city to get weather information.
   - View weather trends through a graphical representation.
   - Get suggestions for cities as you type.

## API Endpoints

### `/`

- **Method**: `GET`, `POST`
- **Description**: The homepage where users can search for weather by city.

### `/location_weather`

- **Method**: `GET`
- **Description**: Fetch weather data based on latitude and longitude.

### `/weather_graph`

- **Method**: `GET`
- **Description**: Display a graph of weather trends for multiple days (Temperature, Humidity, Wind Speed).

### `/weather`

- **Method**: `GET`
- **Description**: Fetch detailed weather information for a specified city.

### `/suggest-cities`

- **Method**: `GET`
- **Description**: Get city suggestions based on partial input.

## Example

1. **Search Weather by City**: 
   Enter a city name, and get the current temperature, weather description, humidity, and wind speed.

2. **View Weather Trends**: 
   See how the temperature, humidity, and wind speed change over the next few days.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Feel free to adjust the details as needed, especially the GitHub repository link and any other specific project details!
