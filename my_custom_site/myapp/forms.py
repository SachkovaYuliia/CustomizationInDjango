# 2. Напишіть форму із кастомним валідатором.
# Створіть віджет користувача (наприклад, кастомний селект).

from django import forms
from .widgets import CustomSelectWidget
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, CustomModel
from django.core.exceptions import ValidationError
import re

class CustomSelectForm(forms.Form):
    option = forms.ChoiceField(
        label="select option",
        choices=[('1', 'Option 1'), ('2', 'Option 2'), ('3', 'Option 3')],
        widget=CustomSelectWidget
    )

class CustomUserRegistrationForm(UserCreationForm):
    """
    Форма реєстрації користувача з кастомною валідацією.
    """
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(required=True, max_length=15)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone_number', 'password1', 'password2')

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not phone_number.isdigit():
            raise forms.ValidationError("Phone number must contain only digits.")
        if len(phone_number) < 10:
            raise forms.ValidationError("Phone number must be at least 10 digits long.")
        return phone_number

