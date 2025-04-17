import requests
import logging
from django.core.management.base import BaseCommand
from django.db import transaction
from weather.models import WeatherRecord
from tqdm import tqdm  # For progress bar

# Set up logging
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Fetch and insert weather data for all regions and parameters'

    def handle(self, *args, **options):
        # List of all regions
        regions = ['UK', 'ENGN', 'SCT', 'WLS', 'NI']
        # List of all parameters
        parameters = ['Tmax', 'Tmin', 'Rainfall', 'Sunshine', 'Tmean', 'AirFrost']
        
        for region in regions:
            for parameter_name in parameters:
                self.fetch_and_insert_data(region, parameter_name)

    def fetch_and_insert_data(self, region_name, parameter_name):
        url = f'https://www.metoffice.gov.uk/pub/data/weather/uk/climate/datasets/{parameter_name}/date/{region_name}.txt'
        self.stdout.write(self.style.SUCCESS(f"📡 Fetching data for {parameter_name} in {region_name} from: {url}"))

        try:
            response = requests.get(url)
            response.raise_for_status()
            lines = response.text.strip().split('\n')

            # Determine correct header lines to skip
            data_lines = lines[7:]  # You may adjust this if needed
            self.stdout.write(self.style.SUCCESS(f"📄 {len(data_lines)} data lines fetched for {parameter_name} in {region_name}."))

        except requests.exceptions.RequestException as e:
            self.stderr.write(self.style.ERROR(f"❌ Failed to fetch {parameter_name} for {region_name}: {e}"))
            logger.error(f"Failed to fetch {parameter_name} for {region_name}: {e}")
            return

        # Optional: Delete old data for the parameter and region
        deleted_count, _ = WeatherRecord.objects.filter(
            region_name=region_name, parameter_name=parameter_name).delete()
        self.stdout.write(self.style.WARNING(f"🧹 Deleted {deleted_count} old records for {region_name} - {parameter_name}"))

        inserted_count = 0
        # Use transaction to ensure batch insertion is atomic
        with transaction.atomic():
            records_to_insert = []
            for line_number, line in enumerate(data_lines, start=1):
                parts = line.split()
                if len(parts) >= 2:
                    try:
                        year = int(parts[0])
                        values = [self.parse_value(val) for val in parts[1:]]
                        values += [None] * (13 - len(values))  # Ensure always 13 elements

                        records_to_insert.append(WeatherRecord(
                            year=year,
                            region_name=region_name,
                            parameter_name=parameter_name,
                            jan=values[0], feb=values[1], mar=values[2],
                            apr=values[3], may=values[4], jun=values[5],
                            jul=values[6], aug=values[7], sep=values[8],
                            oct=values[9], nov=values[10], dec=values[11],
                            annual=values[12]
                        ))
                        inserted_count += 1
                    except Exception as e:
                        self.stderr.write(self.style.ERROR(
                            f"❌ Error saving line {line_number} ({parameter_name} for {region_name}): {e}"))
                        logger.error(f"Error saving line {line_number} ({parameter_name} for {region_name}): {e}")
                else:
                    self.stderr.write(self.style.WARNING(
                        f"⚠️ Skipping line {line_number} for {parameter_name} in {region_name}: {line}"))

            # Insert all records in bulk
            WeatherRecord.objects.bulk_create(records_to_insert, batch_size=500)
            self.stdout.write(self.style.SUCCESS(f"✅ Finished inserting {inserted_count} records for {parameter_name} in {region_name}"))

    @staticmethod
    def parse_value(val):
        """Parse individual cell values, return None if invalid."""
        try:
            return float(val) if val not in ['', 'NaN'] else None
        except ValueError:
            return None
