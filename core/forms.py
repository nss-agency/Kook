from django import forms
from django.forms import ModelForm
from .models import Booking, Banquet


class BookingForm(ModelForm):
    """
    Add Booking object form
    """
    phone = forms.CharField(label='Номер телефону',
                            widget=forms.TextInput,
                            max_length=100,
                            required=True)

    class Meta:
        model = Booking
        fields = (
            'pib',
            'phone',
            'email',
            'date_entry',
            'date_leave',
            'quantity',
            'room_type',
            'additional',
            'breakfest',
            'discount',
        )
        widgets = {
            'pib': forms.TextInput,
            'phone': forms.TextInput,
            'email': forms.EmailInput,
            'date_entry': forms.SelectDateWidget,
            'date_leave': forms.SelectDateWidget,
            'quantity': forms.NumberInput,
        }
        labels = {
            'room_type': 'Тип кімнати'
        }


class BanquetForm(ModelForm):
    phone = forms.CharField(label='Номер телефону',
                            widget=forms.TextInput,
                            max_length=100,
                            required=True)

    class Meta:
        model = Banquet
        fields = (
            'pib',
            'phone',
            'email',
            'check_in',
        )
        widgets = {
            'pib': forms.TextInput,
            'phone': forms.TextInput,
            'email': forms.EmailInput,
            'check_in': forms.SelectDateWidget,
        }
