from django import forms

from rae.models import BusinessCard


class LoginForm(forms.Form):
    username = forms.CharField(label="Login")
    password = forms.CharField(label="Hasło", widget=forms.PasswordInput)


class RegisterForm(LoginForm):
    def clean_username(self):
        username = self.cleaned_data["username"]
        if BusinessCard.objects.filter(username=username).exists():
            raise forms.ValidationError("Podany login jest zajęty.")
        return username


class BusinessCardForm(forms.ModelForm):
    def clean_url(self):
        url = self.cleaned_data["url"]
        if BusinessCard.objects.filter(url=url).exists():
            suggested_url = f"{url}_{self.instance.pk}"
            raise forms.ValidationError(
                f"Podany adres już istnieje. Wybierz inną nazwę, np. {suggested_url}"
            )
        url_name = url.replace(" ", "").lower()
        url = f"https://card.ceremeo.pl/{url_name}"
        return url

    class Meta:
        model = BusinessCard
        fields = ("name", "company", "phone", "email", "photo", "url")


class LPStep1Form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["phone"].label = False
        self.fields["phone"].widget.attrs[
            "placeholder"
        ] = "Wpisz swój numer telefonu..."

    class Meta:
        model = BusinessCard
        fields = ("phone",)
