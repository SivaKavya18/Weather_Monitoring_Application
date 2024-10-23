import requests
import time
import schedule
import smtplib
from datetime import datetime
from collections import defaultdict
import matplotlib.pyplot as plt

API_KEY = 'b00ee7892e9e55b72adb29f3d82ada98'  # Replace with your API Key
CITIES = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']
THRESHOLD_TEMP = 35  # Example threshold for temperature in Celsius
CHECK_INTERVAL = 300  # Time interval to fetch data (in seconds, e.g., 5 minutes)
DAILY_DATA = defaultdict(list)  # To store weather data for daily aggregation

# Function to convert temperature from Kelvin to Celsius
def kelvin_to_celsius(kelvin):
    return kelvin - 273.15

# Function to fetch weather data
def fetch_weather_data():
    for city in CITIES:
        response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}')
        data = response.json()

        if response.status_code == 200:
            temp = kelvin_to_celsius(data['main']['temp'])
            feels_like = kelvin_to_celsius(data['main']['feels_like'])
            main_condition = data['weather'][0]['main']
            timestamp = datetime.utcfromtimestamp(data['dt']).strftime('%Y-%m-%d %H:%M:%S')

            print(f"[{timestamp}] {city} - Temp: {temp:.2f}°C, Feels Like: {feels_like:.2f}°C, Condition: {main_condition}")
            DAILY_DATA[city].append({
                'temp': temp,
                'feels_like': feels_like,
                'main': main_condition,
                'timestamp': timestamp
            })

            # Check alert conditions
            if temp > THRESHOLD_TEMP:
                trigger_alert(city, temp)

# Function to trigger alerts
def trigger_alert(city, temp):
    print(f"ALERT: Temperature in {city} has exceeded {THRESHOLD_TEMP}°C! Current Temp: {temp:.2f}°C")

    # You can also implement an email alert system here
    # send_email_alert(city, temp)

# Function to roll up daily summary and save the data
def calculate_daily_summary():
    for city, records in DAILY_DATA.items():
        if records:
            daily_temps = [record['temp'] for record in records]
            dominant_condition = max(set([record['main'] for record in records]), key=[record['main'] for record in records].count)

            daily_summary = {
                'avg_temp': sum(daily_temps) / len(daily_temps),
                'max_temp': max(daily_temps),
                'min_temp': min(daily_temps),
                'dominant_condition': dominant_condition,
                'date': datetime.now().strftime('%Y-%m-%d')
            }

            print(f"Daily Summary for {city}: {daily_summary}")
            store_daily_summary(city, daily_summary)
            visualize_weather(city)
        # Clear today's data after summarizing
        DAILY_DATA[city].clear()

# Function to store daily summary (you can implement a database or file-based storage)
def store_daily_summary(city, summary):
    with open(f'{city}_weather_summary.txt', 'a') as f:
        f.write(f"{summary['date']} - Avg: {summary['avg_temp']:.2f}°C, Max: {summary['max_temp']:.2f}°C, Min: {summary['min_temp']:.2f}°C, Condition: {summary['dominant_condition']}\n")

# Function to visualize weather trends
def visualize_weather(city):
    records = DAILY_DATA[city]
    if not records:
        print(f"No data available for {city}")
        return

    timestamps = [record['timestamp'] for record in records]
    temps = [record['temp'] for record in records]

    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, temps, label='Temperature (°C)', color='blue')
    plt.xticks(rotation=45)
    plt.title(f"Temperature Trend for {city}")
    plt.xlabel('Time')
    plt.ylabel('Temperature (°C)')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
# Scheduler to fetch weather data every 5 minutes
schedule.every(CHECK_INTERVAL).seconds.do(fetch_weather_data)
# Scheduler to calculate daily summary at the end of the day
schedule.every().day.at("23:59").do(calculate_daily_summary)

def main():
  fetch_weather_data()
  calculate_daily_summary()
  while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
