from django.shortcuts import render
from .models import WeatherRecord

def weather_view(request):
    # Define the possible regions and parameters
    regions = ['UK', 'ENGN', 'SCT', 'WLS', 'NIR']  # List of regions based on the Met Office site
    parameters = ['Tmax', 'Tmin', 'Rainfall', 'Sunshine', 'Wind Speed', 'Humidity']  # List of parameters

    # Get the selected region and parameter from the request GET
    selected_region = request.GET.get('region_name')
    selected_parameter = request.GET.get('parameter_name')
    
    # Initialize records to None (in case there are no records matching the filter)
    records = None

    # If both region and parameter are selected, filter the records
    if selected_region and selected_parameter:
        records = WeatherRecord.objects.filter(
            region_name=selected_region,
            parameter_name=selected_parameter
        ).order_by('-year')

    # Pass the regions, parameters, selected region, selected parameter, and records to the template
    return render(request, 'weather/weather.html', {
        'regions': regions,
        'parameters': parameters,
        'selected_region': selected_region,
        'selected_parameter': selected_parameter,
        'records': records,
    })
