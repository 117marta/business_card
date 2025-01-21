from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from rae.forms import BusinessCardForm, LoginForm, LPStep1Form, RegisterForm
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
    next_page = request.GET.get("next")

    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            if business_card := authenticate(username=username, password=password):
                login(request, business_card)
                if next_page:
                    return redirect(next_page)
                else:
                    return redirect("generate-data")
            else:
                messages.error(request, "Nieprawidłowy login lub hasło.")
        else:
            messages.error(request, "Błędy w formularzu.")

    return render(request, "rae/login.html", {"form": form})


@login_required
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


@login_required
def display_data(request):
    business_card = get_object_or_404(BusinessCard, pk=request.user.pk)
    url = business_card.url
    qr = generate_qr(url)
    return render(request, "rae/display_data.html", {"url": url, "qr": qr})


def lp_step1(request, url):
    business_card = get_object_or_404(BusinessCard, url=url)
    form = LPStep1Form(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            return redirect("index")
    return render(
        request, "rae/lp_step1.html", {"business_card": business_card, "form": form}
    )


def lp_step4(request):
    mem = "https://picsum.photos/600/400"
    return render(request, "rae/lp_step4.html", {"mem": mem})
