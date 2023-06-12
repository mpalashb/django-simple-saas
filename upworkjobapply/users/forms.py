from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy as _

from users.models import (
    Profile
)


class ModifyUserCreationForm(UserCreationForm):
    username = forms.CharField(
        max_length=225, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", 'class': 'form-control'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", 'class': 'form-control'}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )


class GenCoverForm(forms.Form):
    title = forms.CharField(max_length=2500)
    desc = forms.CharField(max_length=2500)
    client = forms.CharField(label='Client Name (optional)', required=False)
    type_option = forms.ChoiceField(label='Generate Type (optional)', choices=(("normal", "Normal"),
                                                                               ("short",
                                                                                "Short"),
                                                                               ("very_short",
                                                                                "Very Short"),
                                                                               ), required=False,)


class ProfileForm(forms.ModelForm):
    email = forms.EmailField(max_length=225, widget=forms.EmailInput(
        attrs={'class': 'form-control', 'style': 'min-width: 603px;'}))
    first_name = forms.CharField(
        max_length=225, widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'min-width: 603px;'}),)
    last_name = forms.CharField(
        max_length=225, widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'min-width: 603px;'}))
    company = forms.CharField(max_length=225, widget=forms.TextInput(
        attrs={'class': 'form-control', 'style': 'min-width: 603px;'}),)

    class Meta:
        model = Profile
        exclude = ("user", "credit", )
