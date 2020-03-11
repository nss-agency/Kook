from django.shortcuts import render, redirect
from .forms import BookingForm
from .models import Booking, RoomType
from .decorators import check_recaptcha
import datetime


# def is_room_type_available(room_type, date_entry, date_leave):
#     # case 1: a room is booked before the check_in date, and checks out after the requested check_in date
#


# Create your views here.
def index(request):
    ctx = {}

    return render(request, 'index.html', ctx)


def form(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            ctx2 = {
                'success': False,
                'fail': False,

            }
            date_entry = form.cleaned_data['date_entry']
            date_leave = form.cleaned_data['date_leave']
            room_type = form.cleaned_data['room_type']

            case_1 = Booking.objects.filter(room_type=room_type, date_entry__lte=date_entry,
                                            date_leave__gte=date_entry).exists()

            case_2 = Booking.objects.filter(room_type=room_type, date_entry__lte=date_leave,
                                            date_leave__gte=date_leave).exists()

            case_3 = Booking.objects.filter(room_type=room_type, date_entry__lte=date_entry,
                                            date_leave__gte=date_leave).exists()

            case_4 = Booking.objects.filter(room_type=room_type, date_entry__gte=date_entry,
                                            date_leave__lte=date_leave).exists()

            if case_1 or case_2 or case_3 or case_4:
                print('hello')
                ctx2['fail'] = True
            else:
                booking = form.save(commit=False)
                booking.save()
                ctx2['success'] = True
        else:
            BookingForm()

    ctx = {
        'form': BookingForm,
        'ctx2': ctx2
    }

    return render(request, 'form.html', ctx)
