from django.shortcuts import render, redirect, get_object_or_404
from .managers import fetch_tourist_attractions, generate_traditional_foods, generate_itinerary, fetch_weather_information
from .forms import RegionForm, PlacesForm
from .models import Itinerary, ItineraryEntry, FoodList

from datetime import date, timedelta, datetime


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

    if region_name:
        places_list = fetch_tourist_attractions(region_name)
        form = PlacesForm(initial={'region_name': region_name}, places_list=places_list)
        if request.method == 'POST':
            form = PlacesForm(request.POST, initial={'region_name': region_name}, places_list=places_list)
            if form.is_valid():
                selected_places = form.cleaned_data['selected_places']
                request.session['selected_places'] = selected_places
                return redirect('generate_itinerary')
    else:
        return redirect('choose_region')
    
    return render(request, 'api_manager/choose_places.html', {'form': form})


def generate_itinerary_view(request):
    region_name = request.session.get('region_name', None)
    selected_places = request.session.pop('selected_places', None)
    start_date = request.session.pop('start_date', None)
    end_date = request.session.pop('end_date', None)

    start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

    if not start_date > date.today() + timedelta(days=10):
        weather_info = fetch_weather_information(region_name, start_date, end_date)
        avgtemp_list, avg_humidity_list, rain_probability_list, snow_probability_list = weather_info
        is_weather_info = True
    else:
        is_weather_info = False

    duration = (end_date - start_date).days + 1
    date_list = [start_date + timedelta(days=i) for i in range(duration)]

    if region_name and start_date and end_date and selected_places:
        if is_weather_info:
            itinerary = generate_itinerary(region_name, date_list, selected_places, duration, avgtemp_list, avg_humidity_list, rain_probability_list, snow_probability_list)
            context = {
            'region_name': region_name,
            'itinerary': itinerary,
            'date_list': date_list,
            'avgtemp_list': avgtemp_list,
            'avg_humidity_list': avg_humidity_list,
            'rain_probability_list': rain_probability_list,
            'snow_probability_list': snow_probability_list,
            'is_weather_info': is_weather_info,
        }
            
        else:
            itinerary = generate_itinerary(region_name, date_list, selected_places, duration)
            context = {
                'region_name': region_name,
                'itinerary': itinerary,
                'date_list': date_list,
                'is_weather_info': is_weather_info,
            }

        

        return render(request, 'api_manager/generate_itinerary.html', context=context)
    
    elif region_name and start_date and end_date:
        return redirect('choose_places')
    
    else:
        return redirect('choose_region')


def save_itinerary_entries(request):
    if request.method == 'POST':
        itinerary_name = request.POST.get('itinerary_name')
        itinerary = Itinerary.objects.create(name=itinerary_name, user=request.user)

        date_list = request.POST.getlist('date')
        activity_list = request.POST.getlist('activity')
        is_weather_info = request.POST.get('is_weather_info')
        
        if is_weather_info == True:
            avgtemp_list = request.POST.getlist('avgtemp')
            avg_humidity_list = request.POST.getlist('avg_humidity')
            rain_probability_list = request.POST.getlist('rain_probability')
            snow_probability_list = request.POST.getlist('snow_probability')

            for i in range(len(date_list)):
                entries = ItineraryEntry(
                    date=date_list[i],
                    avgtemp=avgtemp_list[i],
                    avg_humidity=avg_humidity_list[i],
                    rain_probability=rain_probability_list[i],
                    snow_probability=snow_probability_list[i],
                    activity=activity_list[i],
                    itinerary=itinerary
                )
                entries.save()
        else:
            for i in range(len(date_list)):
                entries = ItineraryEntry(
                    date=date_list[i],
                    activity=activity_list[i],
                    itinerary=itinerary
                )
                entries.save()
        
        return redirect('foods', itinerary_id=itinerary.id)
    
    return render(request, 'api_manager/generate_itinerary.html')


def create_food_list(request, itinerary_id):
    region_name = request.session.pop('region_name', None)

    if region_name:
        itinerary = get_object_or_404(Itinerary, pk=itinerary_id)
        foods = generate_traditional_foods(region_name)
        for food, description in foods.items():
            food_list = FoodList(name=food, description=description, itinerary=itinerary)
            food_list.save()

        return redirect('itinerary_detail', itinerary_id=itinerary.id)
    
    else:
        return redirect('choose_region')


def itinerary_detail(request, itinerary_id):
    itinerary = get_object_or_404(Itinerary, pk=itinerary_id)
    entries = itinerary.itinerary_entries.all()
    foods = itinerary.food_list.all()
    return render(request, 'api_manager/itinerary_detail.html', {'itinerary': itinerary, 'entries': entries, 'foods': foods})


def update_itinerary(request, itinerary_id):
    itinerary = get_object_or_404(Itinerary, pk=itinerary_id)
    entries = itinerary.itinerary_entries.all()

    if request.method == 'POST':
        itinerary_name = request.POST.get('itinerary_name')
        itinerary.name = itinerary_name
        itinerary.save()

        updated_activities = request.POST.getlist('activity')
        entries_id = request.POST.getlist('entry_id')
        for i in range(len(entries_id)):
            entry = get_object_or_404(ItineraryEntry, pk=entries_id[i])
            entry.activity = updated_activities[i]
            entry.save()

        return redirect('itinerary_detail', itinerary_id=itinerary.id)

    return render(request, 'api_manager/update_itinerary.html', {'itinerary': itinerary, 'entries': entries})


def delete_itinerary(request, itinerary_id):
    itinerary = get_object_or_404(Itinerary, pk=itinerary_id)

    if request.method == 'POST':
        itinerary.delete()
        return redirect('/')
    
    return render(request, 'delete_item.html', {'itinerary': itinerary})


def itinerary_list(request):
    itineraries = Itinerary.objects.filter(user=request.user)
    return render(request, 'api_manager/itinerary_list.html', {'itineraries': itineraries})