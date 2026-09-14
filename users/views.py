from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from podcasts.models import Favorite
from .registration import RegisterForm
from django.contrib.auth import login

@login_required
def profile(request):
    favorites = request.user.favorite_podcasts.all()
    return render(request, 'users/profile.html', {'favorites': favorites})

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # auto login after register
            return redirect('home')  # change if needed
    else:
        form = RegisterForm()

    return render(request, 'users/register.html', {'form': form})