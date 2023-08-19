from django.shortcuts import render, redirect
from .managers import fetch_tourist_attractions, generate_traditional_foods, generate_itinerary, fetch_weather_info
from .forms import RegionForm, PlacesForm, FoodsForm

from datetime import date, timedelta


def choose_region(request):
    if request.method == 'POST':
        form = RegionForm(request.POST)
        if form.is_valid():
            region_name = form.cleaned_data['region_name']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            request.session['region_name'] = region_name
            request.session['start_date'] = start_date.strftime("%Y-%m-%d")
            request.session['end_date'] = end_date.strftime("%Y-%m-%d")
            return redirect('choose_places')
    else:
        form = RegionForm()
    
    return render(request, 'api_manager/choose_region.html', {'form': form})


def choose_places(request):
    region_name = request.session.get('region_name')
    places_list = fetch_tourist_attractions(region_name)

    if region_name:
        form = PlacesForm(initial={'region_name': region_name}, places_list=places_list)
        if request.method == 'POST':
            form = PlacesForm(request.POST, initial={'region_name': region_name}, places_list=places_list)
            if form.is_valid():
                selected_places = form.cleaned_data['selected_places']
                request.session['selected_places'] = selected_places
                return redirect('choose_foods')
    else:
        return redirect('choose_region')
    
    return render(request, 'api_manager/choose_places.html', {'form': form})


def choose_foods(request):
    region_name = request.session.get('region_name')
    selected_places = request.session.get('selected_places')
    foods_list = generate_traditional_foods(region_name)

    if region_name and selected_places:
        form = FoodsForm(initial={'region_name': region_name, 'selected_places': selected_places}, foods_list=foods_list)
        if request.method == 'POST':
            form = FoodsForm(request.POST, foods_list=foods_list)
            if form.is_valid():
                selected_foods = form.cleaned_data['selected_foods']
                request.session['selected_foods'] = selected_foods
                return redirect('itinerary_view')
        
    elif region_name:
        return redirect('choose_places')
    
    else:
        return redirect('choose_region')
    
    return render(request, 'api_manager/choose_foods.html', {'form': form})


def itinerary_view(request):
    region_name = request.session.get('region_name')
    selected_places = request.session.get('selected_places')
    selected_foods = request.session.get('selected_foods')
    start_date = request.session.get('start_date')
    end_date = request.session.get('end_date')

    if not start_date.strptime("%Y-%m-%d").date() > date.today() + timedelta(days=10):
        weather_info = fetch_weather_info(region_name, start_date, end_date)
    else:
        weather_info = None

    duration = (end_date - start_date).days + 1

    if region_name and selected_places and selected_foods:
        itinerary = generate_itinerary(region_name, selected_places, duration, weather_info)
        context = {
            'region_name': region_name,
            'selected_places': selected_places,
            'selected_foods': selected_foods,
            'itinerary': itinerary
        }
        return render(request, 'api_manager/itinerary.html', context)
    
    elif region_name and selected_places:
        return redirect('choose_foods')
    
    elif region_name:
        return redirect('choose_places')
    
    else:
        return redirect('choose_region')
