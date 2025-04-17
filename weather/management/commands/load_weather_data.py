from django.core.management.base import BaseCommand
from weather.models import WeatherData
from weather.parser import parse_weather_data

class Command(BaseCommand):
    help = 'Load weather data into the database'

    def handle(self, *args, **kwargs):
        df = parse_weather_data()

        # Print the columns and first few rows for debugging
        print("Columns in DataFrame:", df.columns)
        print("First few rows of DataFrame:\n", df.head())

        for _, row in df.iterrows():
            # Check if 'year' exists in the current row
            if 'year' in row:
                WeatherData.objects.update_or_create(
                    year=row['year'],
                    defaults=row.to_dict()
                )
            else:
                print(f"Warning: 'year' not found in row: {row}")
        
        self.stdout.write("Weather data loaded successfully.")
