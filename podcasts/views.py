from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages

from .forms import LoginForm, RegisterForm


# Create your views here.
def view_podcasts(request):
    return HttpResponse(f"hi")


def login_view(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('home')

        form = LoginForm()
        return render(request, 'podcast/login.html', {'form': form})

    elif request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f'Hi {username.title()}, welcome back!')
                return redirect('home')

        # either form not valid or user is not authenticated
        messages.error(request, f'Invalid username or password')
        return render(request, 'podcast/login.html', {'form': form})


def register_view(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'podcast/register.html', {'form': form})

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'You have singed up successfully.')
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'podcast/register.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, f'You have been logged out.')
    return redirect('login')
