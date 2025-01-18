from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render

from rae.forms import LoginForm, RegisterForm
from rae.models import BusinessCard


def index(request):
    return render(request, 'rae/index.html')


def register_view(request):
    form = RegisterForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            BusinessCard.objects.create_user(username=username, password=password)
            messages.success(request, "Utworzono konto! Zaloguj się.")
            return redirect("login")
        else:
            messages.error(request, "Błędy w formularzu.")

    return render(request, "rae/register.html", {"form": form})


def login_view(request):
    form = LoginForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            if business_card := authenticate(username=username, password=password):
                login(request, business_card)
                messages.success(request, "Zalogowano! Wypełnij dane.")
            else:
                messages.error(request, "Nieprawidłowy login lub hasło.")
        else:
            messages.error(request, "Błędy w formularzu.")

    return render(request, "rae/login.html", {"form": form})
