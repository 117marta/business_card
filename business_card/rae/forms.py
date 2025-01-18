from django import forms

from rae.models import BusinessCard


class LoginForm(forms.Form):
    username = forms.CharField(label='Login')
    password = forms.CharField(label='Hasło', widget=forms.PasswordInput)


class RegisterForm(LoginForm):
    def clean_username(self):
        business_card = self.cleaned_data["username"]
        if BusinessCard.objects.filter(username=business_card).exists():
            raise forms.ValidationError("Podany login jest zajęty.")
        return business_card
