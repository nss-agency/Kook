from django import forms
from django.forms import ModelForm
from .models import Booking, Banquet
from datetime import datetime


class BookingForm(ModelForm):
    """
    Add Booking object form
    """

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
            'pib': forms.TextInput(attrs={
                'placeholder': ' '
            }),
            'phone': forms.TextInput(attrs={
                'type': 'tel',
                'placeholder': ' '
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': ' '
            }),
            'date_entry': forms.TextInput(attrs={
                'type': 'text',
                'placeholder': ' ',
                'onfocus': "(this.type='date')",
                'onblur': "(this.type='text')",
                'min': "(datetime.now())"
            }),
            'date_leave': forms.TextInput(attrs={
                'type': 'text',
                'placeholder': ' ',
                'onfocus': "(this.type='date')",
                'onblur': "(this.type='text')",
                'min': "(datetime.now())"
            }),
            'quantity': forms.NumberInput(attrs={
                'placeholder': ' ',
                'min': 1,
                'step': 1,
            }),
            'discount': forms.TextInput(attrs={
                'placeholder': ' '
            }),
            'room_type': forms.Select(attrs={
                'hidden': 'false'
            }),
            'additional': forms.TextInput(attrs={
                'placeholder': ' '
            }),
            'breakfest': forms.HiddenInput
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
            'check_in': forms.TextInput(attrs={
                'type': 'date',
            }),
        }
