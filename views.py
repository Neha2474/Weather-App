from django.shortcuts import redirect
import requests
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import searchWeather

API_KEY = "038358d882b4533bb3347177bf30c178"

def weathers(request):

    weather = None
    error = None
    searches = searchWeather.objects.order_by('-date')[:5]

    if request.method == 'POST':
        city = request.POST.get('city', '').strip()

        if "clearAll" in request.POST:
            searchWeather.objects.all().delete()
            return redirect("weather")

        if city:

            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

            try:
                resp = requests.get(url, timeout=5)
                data = resp.json()

                if resp.status_code == 200:
                    weather = {
                        'city': f"{data['name']},{data['sys']['country']}",
                        'humidity' : data['main']['humidity'],
                        'temperature' : data['main']['temp'],
                        'pressure': data['main']['pressure'],
                        'description' : data['weather'][0] ['description'].title(),
                        'icon': data['weather'][0]['icon'],
                    }
                    searchWeather.objects.create(
                        city = data['name'],
                        temperature = data['main']['temp'],
                        humidity = data['main']['humidity'],
                        pressure = data['main']['temp'],
                        description = data['weather'][0]['description'].title()
                    )
                    searches = searchWeather.objects.order_by('-date')[:5]
                else:
                    error = data.get("message","Could Not Fetch Weather Data.")


            except Exception as e:
                    error = str(e)
        else:
            error = "Please enter a city name."

    #template = loader.get_template('weather_page.html')
    return render(request, 'weather_page.html', {'error': error, 'weather':weather,'searches':searches})