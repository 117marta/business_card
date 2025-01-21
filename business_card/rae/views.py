from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from formtools.wizard.views import SessionWizardView

from rae.forms import (
    BusinessCardForm,
    LoginForm,
    RegisterForm,
    Step1Form,
    Step2Form,
    Step3Form,
)
from rae.helpers import generate_qr, send_data_to_ceremeo
from rae.models import BusinessCard

URL = "https://url_systemu/api/v1/lead/"


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


class LPMultistepView(SessionWizardView):
    TEMPLATES = {
        "0": "rae/lp_multistep1.html",
        "1": "rae/lp_multistep2.html",
        "2": "rae/lp_multistep3.html",
    }
    form_list = [Step1Form, Step2Form, Step3Form]

    def get_template_names(self):
        return [self.TEMPLATES[self.steps.current]]

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        url = self.kwargs.get("url")
        business_card = get_object_or_404(BusinessCard, url=url)
        if self.steps.current == "0":
            context.update({"business_card": business_card})
        return context

    def get_next_step(self, step=None):
        all_cleaned_data = self.get_all_cleaned_data()
        if settings.SEND_TO_CEREMEO:
            send_data_to_ceremeo(payload=all_cleaned_data, url=URL)
        return super().get_next_step(step)


    def done(self, form_list, **kwargs):
        form_data_dict = self.get_all_cleaned_data()
        if settings.SEND_TO_CEREMEO:
            send_data_to_ceremeo(payload=form_data_dict, url=URL)
        return redirect("lp-step4")


def lp_step4(request):
    mem = "https://picsum.photos/600/400"
    return render(request, "rae/lp_step4.html", {"mem": mem})
