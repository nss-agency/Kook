from django.shortcuts import render
from .forms import BookingForm
from .models import Booking, RoomType
from .decorators import check_recaptcha
import datetime


def is_room_type_available(room_type, date_entry, date_leave):
    bookings = Booking.objects.filter(room_type=room_type, date_entry__lte=date_entry,
                                      date_leave__lte=date_entry).union(
        Booking.objects.filter(room_type=room_type, date_entry__gte=date_leave, date_leave__gte=date_leave))
    return bookings


# Create your views here.
def index(request):
    ctx = {}

    return render(request, 'index.html', ctx)


def form(request):
    """
     Create object by form via Booking model
    """

    print(is_room_type_available(RoomType.objects.get(pk=1), datetime.datetime(2020, 3, 8, 13, 0, 0),
                                 datetime.datetime(2020, 3, 15, 13, 0, 0)))

    if request.method == 'POST':
        f = BookingForm(request.POST)
        if f.is_valid():
            booking = f.save(commit=False)
            booking.save()
        else:
            BookingForm()

    ctx = {
        'form': BookingForm
    }

    return render(request, 'form.html', ctx)
