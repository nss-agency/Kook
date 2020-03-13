from django.shortcuts import render, redirect
from .forms import BookingForm
from .models import Booking, RoomType
from .decorators import check_recaptcha
import datetime


# Create your views here.
def index(request):
    ctx = {}

    return render(request, 'index.html', ctx)


def hotel(request):
    ctx2 = {
        'success': False,
        'fail': False,
    }
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
                                            date_leave__gte=date_entry)

            case_2 = Booking.objects.filter(room_type=room_type, date_entry__lte=date_leave,
                                            date_leave__gte=date_leave)

            case_3 = Booking.objects.filter(room_type=room_type, date_entry__lte=date_entry,
                                            date_leave__gte=date_leave)

            case_4 = Booking.objects.filter(room_type=room_type, date_entry__gte=date_entry,
                                            date_leave__lte=date_leave)

            case = (case_1.union(case_2).union(case_3).union(case_4)).count()

            if (case_1 or case_2 or case_3 or case_4) and case >= room_type.quantity:
                print('Zanyato')
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
    return render(request, 'hotel_rooms.html', ctx)


def form(request):
    ctx2 = {
        'success': False,
        'fail': False,
    }
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
                                            date_leave__gte=date_entry)

            case_2 = Booking.objects.filter(room_type=room_type, date_entry__lte=date_leave,
                                            date_leave__gte=date_leave)

            case_3 = Booking.objects.filter(room_type=room_type, date_entry__lte=date_entry,
                                            date_leave__gte=date_leave)

            case_4 = Booking.objects.filter(room_type=room_type, date_entry__gte=date_entry,
                                            date_leave__lte=date_leave)

            case = (case_1.union(case_2).union(case_3).union(case_4)).count()

            if (case_1 or case_2 or case_3 or case_4) and case >= room_type.quantity:
                print('Zanyato')
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
