from django.db import models

class WeatherRecord(models.Model):
    year = models.IntegerField()
    region_name = models.CharField(max_length=100)
    parameter_name = models.CharField(max_length=100)
    jan = models.FloatField(null=True, blank=True)
    feb = models.FloatField(null=True, blank=True)
    mar = models.FloatField(null=True, blank=True)
    apr = models.FloatField(null=True, blank=True)
    may = models.FloatField(null=True, blank=True)
    jun = models.FloatField(null=True, blank=True)
    jul = models.FloatField(null=True, blank=True)
    aug = models.FloatField(null=True, blank=True)
    sep = models.FloatField(null=True, blank=True)
    oct = models.FloatField(null=True, blank=True)
    nov = models.FloatField(null=True, blank=True)
    dec = models.FloatField(null=True, blank=True)
    annual = models.FloatField(null=True, blank=True)
    unit = models.CharField(max_length=50, default="Unknown")

    def __str__(self):
        return f"{self.region_name} - {self.parameter_name} ({self.year})"
