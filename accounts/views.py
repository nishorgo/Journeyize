from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate, login

from .forms import RegistrationForm

def user_login(request):
    if request.user.is_authenticated:
        return redirect('itinerary_list')

    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password =request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('itinerary_list')
            else:
                messages.info(request, 'Username OR password is incorrect')
        context = {}
        return render(request, 'accounts/login.html', context)

def user_register(request):
    if request.user.is_authenticated:
        return redirect('itinerary_list')
    
    else:
        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                form.save()

                user = f"{form.cleaned_data.get('first_name')} {form.cleaned_data.get('last_name')}"
                messages.success(request, 'Account was created for ' + user)
                return redirect('login')
        
        else:
            form = RegistrationForm()

        context = {'form': form}
        return render(request, 'accounts/register.html', context)