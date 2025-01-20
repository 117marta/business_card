from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404, redirect, render

from rae.forms import BusinessCardForm, LoginForm, RegisterForm
from rae.helpers import generate_qr
from rae.models import BusinessCard


def index(request):
    return render(request, "rae/index.html")


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
                return redirect("generate-data")
            else:
                messages.error(request, "Nieprawidłowy login lub hasło.")
        else:
            messages.error(request, "Błędy w formularzu.")

    return render(request, "rae/login.html", {"form": form})


def generate_data(request):
    form = BusinessCardForm(
        request.POST or None, files=request.FILES or None, instance=request.user
    )

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("display-data")
        else:
            messages.error(request, "Błędy w formularzu.")

    return render(request, "rae/generate_data.html", {"form": form})


def display_data(request):
    business_card = get_object_or_404(BusinessCard, pk=request.user.pk)
    url = business_card.url
    qr = generate_qr(url)
    return render(request, "rae/display_data.html", {"url": url, "qr": qr})
