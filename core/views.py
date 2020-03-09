from django.shortcuts import render, redirect
from .forms import BookingForm
from .models import Booking, RoomType
from .decorators import check_recaptcha
import datetime


def is_room_type_available(room_type, date_entry, date_leave):
    # case 1: a room is booked before the check_in date, and checks out after the requested check_in date
    case_1 = Booking.objects.filter(room_type=room_type, date_entry__lte=date_entry,
                                    date_leave__gte=date_entry).exists()

    # case 2: a room is booked before the requested check_out date and check_out date is after requested check_out date
    case_2 = Booking.objects.filter(room_type=room_type, date_entry__lte=date_leave,
                                    date_leave__gte=date_leave).exists()

    case_3 = Booking.objects.filter(room_type=room_type, date_entry__gte=date_entry,
                                    date_leave__lte=date_leave).exists()

    if case_1 or case_2 or case_3:
        return print('Zanyato')
    else:
        return print('hello')


# Create your views here.
def index(request):
    ctx = {}

    return render(request, 'index.html', ctx)


def form(request):
    """
     Create object by form via Booking model
    """

    # print(is_room_type_available(RoomType.objects.get(pk=1), datetime.datetime(2020, 3, 20, 13, 0, 0),
    #                              datetime.datetime(2020, 3, 22, 13, 0, 0)))

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            date_entry = form.cleaned_data['date_entry']
            date_leave = form.cleaned_data['date_leave']
            room_type = RoomType.objects.get(pk=1)
            is_room_type_available(room_type, date_entry, date_leave)
            booking = form.save(commit=False)
            booking.save()
        else:
            BookingForm()

    ctx = {
        'form': BookingForm
    }

    return render(request, 'form.html', ctx)
