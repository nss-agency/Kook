from django import forms
from django.forms import ModelForm
from .models import Booking


class BookingForm(ModelForm):
    """
    Add Bokking object form
    """
    phone = forms.CharField(label='Номер телефону',
                                widget=forms.TextInput,
                                max_length=100,
                                required=True)
    class Meta:
        model = Booking
        fields = '__all__'
        widgets = {
            'pib' : forms.TextInput,
            'phone' : forms.TextInput,
            'email' : forms.EmailInput,
            'date_entry' : forms.SelectDateWidget,
            'date_leave' : forms.SelectDateWidget,
            'quantity' : forms.NumberInput,
        }


