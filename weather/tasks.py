# weather_app/tasks.py

from apscheduler.schedulers.background import BackgroundScheduler
import time

def fetch_weather():
    # Placeholder: Replace with your actual weather data fetching logic
    print("Fetching weather data...")

def start_scheduler():
    scheduler = BackgroundScheduler()
    # Schedule 'fetch_weather' to run every hour (you can adjust this interval as needed)
    scheduler.add_job(fetch_weather, 'interval', hours=1)
    scheduler.start()
    print("Scheduler started.")
