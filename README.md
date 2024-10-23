# Weather Monitoring Application
This is a Python-based application that fetches real-time weather data for specified cities using the OpenWeatherMap API, triggers alerts when temperature thresholds are exceeded, and generates daily summaries. The application can also visualize temperature trends for the cities being monitored.

## Features

->Fetches weather data for multiple cities every 5 minutes.

->Checks for temperature thresholds and triggers alerts.

->Generates a daily weather summary for each city.

->Visualizes weather data trends.

->Supports daily data roll-up and summary logging.

## Design Choices

**Data fetching and scheduling**: We use the schedule library to periodically fetch weather data and to perform daily summarization at a set time (23:59).

**Temperature conversion**: Temperatures from the API are provided in Kelvin, so the application converts them to Celsius for better readability.

**Alert system**: The application checks if the current temperature exceeds a predefined threshold and triggers alerts accordingly. You can easily extend the code to send email notifications via SMTP.

**Data visualization**: Weather trends are plotted using matplotlib, allowing the user to see temperature variations throughout the day.

**Data storage**: The daily summary for each city is saved as a text file for later reference.

## Prerequisites
Python 3.7+
OpenWeatherMap API Key (you will need to replace the placeholder key in the code)

## Setup and Installation
#### 1. Clone the repository
```bash
git clone <your-repo-url>
cd <your-repo-directory>
```
#### 2. Set up the environment
You can create a virtual environment and install dependencies using the following steps:

```bash
python -m venv venv
source venv/bin/activate  # For Linux/MacOS
```
For Windows:
```bash
venv\Scripts\activate
```

#### 3. Install the dependencies
The required Python libraries are listed in the requirements.txt file. Install them using:
```bash
pip install -r requirements.txt
```

#### 4. Replace the OpenWeatherMap API Key
In the weather_monitor.py file, replace the placeholder API_KEY with your actual API key from OpenWeatherMap:

```python
API_KEY = 'your_actual_api_key_here'
```

#### 5. Run the Application
Once you've set up your environment and added your API key, you can run the application by executing:

```bash
python weather_monitor.py
```
The application will start fetching weather data at the specified interval (every 5 minutes) and will print alerts when necessary.

#### 6. Visualizing Data
The application uses matplotlib to visualize temperature trends for each city. You can view these trends by calling the visualize_weather() function after data collection
