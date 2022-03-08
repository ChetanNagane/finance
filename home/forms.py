from random import choice
from symtable import Symbol
from django import forms
from .models import Stocks, User


class RegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        "autocomplete": "off",
        "class": "form-control",
        "name": "confirm_password",
        "placeholder": "Confirm Password",
        "type": "password",
    }),)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', ]
        widgets = {
            'username': forms.TextInput(attrs={
                "autocomplete": "off",
                "class": "form-control",
                "name": "username",
                "placeholder": "Username",
                "type": "text",
            }),
            'email': forms.TextInput(attrs={
                "autocomplete": "off",
                "class": "form-control",
                "name": "email",
                "placeholder": "Email",
                "type": "email",
            }),
            'password': forms.PasswordInput(attrs={
                "autocomplete": "off",
                "class": "form-control",
                "name": "password",
                "placeholder": "Password",
                "type": "password",
            }),
        }

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'email', 'password', 'confirm_password']:
            self.fields[fieldname].label = ""
            self.fields[fieldname].help_text = None

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        "autocomplete": "off",
        "class": "form-control",
        "name": "username",
        "placeholder": "Username",
        "type": "text",
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "autocomplete": "off",
        "class": "form-control",
        "name": "password",
        "placeholder": "Password",
        "type": "password",
    }),)


class QuoteForm(forms.Form):
    symbol = forms.CharField(widget=forms.TextInput(attrs={
        "autocomplete": "off",
        "class": "form-control",
        "name": "symbol",
        "placeholder": "Symbol",
        "type": "text",
    }))


class BuyForm(forms.Form):
    symbol = forms.CharField(widget=forms.TextInput(attrs={
        "autocomplete": "off",
        "class": "form-control",
        "name": "symbol",
        "placeholder": "Symbol",
        "type": "text",
    }))
    quantity = forms.IntegerField(min_value=1, widget=forms.NumberInput(attrs={
        "autocomplete": "off",
        "class": "form-control",
        "name": "quantity",
        "placeholder": "Quantity",
        "type": "number",
    }),)


class SellForm(forms.Form):
    choice = [
        ("HINDALCO", "HINDALCO"),
        ("TATASTEEL", "TATASTEEL")
    ]

    symbol = forms.ChoiceField(widget=forms.Select(attrs={
        "autocomplete": "off",
        "class": "form-control",
        "name": "symbol",
        "type": "text",
    }))
    quantity = forms.IntegerField(min_value=1, widget=forms.NumberInput(attrs={
        "autocomplete": "off",
        "class": "form-control",
        "name": "quantity",
        "placeholder": "Quantity",
        "type": "number",
    }),)

    def __init__(self, choice, *args, **kwargs):
        super(SellForm, self).__init__(*args, **kwargs)
        self.fields["symbol"].choices = [(x, x) for x in choice]

    # def __init__(self, choice, *args, **kwargs):
    #     request = kwargs.pop('request', None)
    #     super().__init__(*args, **kwargs)
    #     self.choice = [(x, x) for x in choice]
    #     # if request:
    #     #     user = request.user
    #     #     self.fields['symbol'].queryset = choice
