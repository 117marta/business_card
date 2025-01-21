from django import forms

from rae.models import BusinessCard


class LoginForm(forms.Form):
    username = forms.CharField(label="Login")
    password = forms.CharField(label="Hasło", widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["placeholder"] = field.label
            field.label = False
            field.widget.attrs["class"] = "custom-field"


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
        labels = {
            "name": False,
            "company": False,
            "phone": False,
            "email": False,
            "photo": False,
            "url": False,
        }
        widgets = {
            "name": forms.TextInput(
                attrs={"placeholder": "Twoje imię i nazwisko", "class": "custom-field"}
            ),
            "company": forms.TextInput(
                attrs={"placeholder": "Nazwa firmy", "class": "custom-field"}
            ),
            "phone": forms.TextInput(
                attrs={"placeholder": "Numer telefonu", "class": "custom-field"}
            ),
            "email": forms.TextInput(
                attrs={"placeholder": "Adres e-mail", "class": "custom-field"}
            ),
            "photo": forms.FileInput(
                attrs={
                    "placeholder": "Zdjęcie (najlepiej kwadrat)",
                    "class": "custom-field",
                }
            ),
            "url": forms.TextInput(
                attrs={"placeholder": "Adres vcard", "class": "custom-field"}
            ),
        }


class Step1Form(forms.Form):
    phone = forms.CharField(
        label=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Wpisz swój numer telefonu...",
                "class": "custom-field",
            }
        ),
    )

    def clean_phone(self):
        phone = self.cleaned_data["phone"]
        if len(phone) < 9:
            raise forms.ValidationError("Za krótki numer")
        return phone


class Step2Form(forms.Form):
    name = forms.CharField(
        label=False,
        widget=forms.TextInput(
            attrs={"placeholder": "Twoje imię i nazwisko", "class": "custom-field"}
        ),
    )
    email = forms.EmailField(
        label=False,
        widget=forms.TextInput(
            attrs={"placeholder": "Adres e-mail", "class": "custom-field"}
        ),
    )
    company = forms.CharField(
        label=False,
        widget=forms.TextInput(
            attrs={"placeholder": "Firma/miejsce kontaktu", "class": "custom-field"}
        ),
    )

    def clean_name(self):
        name = self.cleaned_data["name"]
        if name.isdigit():
            raise forms.ValidationError("Nie podawaj cyfr przy nazwie")
        return name


class Step3Form(forms.Form):
    date = forms.CharField(
        label=False,
        widget=forms.TextInput(attrs={"placeholder": "Data", "class": "custom-field"}),
    )
    subject = forms.CharField(
        label=False,
        widget=forms.Textarea(attrs={"placeholder": "Temat", "class": "custom-field"}),
    )
