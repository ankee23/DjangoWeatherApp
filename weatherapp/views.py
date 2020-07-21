import requests
from django.shortcuts import render
from .models import City
from .forms import CityForm


# Create your views here.
def index(request):
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&&appid=577730d73e1c7a9c3433a8270df21d94'
    
    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()
            
    form = CityForm()

    cities = City.objects.all()

    weather_data = []

    for city in cities:

        city_data = requests.get(url.format(city)).json()

        city_weather = {
            'city': city,
            'temprature': city_data.get('main', {}).get('temp', ''),
            'description': city_data.get('weather', [])[0].get('description', ''),
            'icon': city_data.get('weather', [])[0].get('icon', '')
        }

        weather_data.append(city_weather)

    context = {'weather_data': weather_data,'form':form}

    return render(request, 'weatherapp/weather.htm', context)
