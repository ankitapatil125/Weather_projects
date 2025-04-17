from django.test import TestCase
from .models import WeatherRecord

class WeatherRecordTestCase(TestCase):
    def test_weather_record_creation(self):
        record = WeatherRecord.objects.create(
            year=2020, region_name="UK", parameter_name="Tmax", jan=5.5, annual=10.5
        )
        self.assertEqual(record.year, 2020)
        self.assertEqual(record.region_name, "UK")
