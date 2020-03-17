from django.shortcuts import render, redirect
from .forms import BookingForm
from .models import Booking, RoomType, Promo, Baquet
from .decorators import check_recaptcha
import datetime
from datetime import datetime


<<<<<<< HEAD
=======
# def is_room_type_available(room_type, date_entry, date_leave):
#     # case 1: a room is booked before the check_in date, and checks out after the requested check_in date
#

def hotel(request):
    ctx = {}
    return render(request, 'hotel_rooms.html', ctx)


>>>>>>> a97e8315806c6c2cf839498754a1d526f28b9e50
# Create your views here.
def index(request):
    ctx = {}
    return render(request, 'index.html', ctx)


<<<<<<< HEAD
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
=======
def banquet(request):
    ctx = {}
    return render(request, 'banquet.html', ctx)
>>>>>>> a97e8315806c6c2cf839498754a1d526f28b9e50


def form(request):
    booking_status = {
        'success': False,
        'fail': False,
    }

    booking_info = {}
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
<<<<<<< HEAD
            ctx2 = {
                'success': False,
                'fail': False,
            }
=======
            pib = form.cleaned_data['pib']
            phone = form.cleaned_data['phone']
            email = form.cleaned_data['email']
>>>>>>> a97e8315806c6c2cf839498754a1d526f28b9e50
            date_entry = form.cleaned_data['date_entry']
            date_leave = form.cleaned_data['date_leave']
            quantity = form.cleaned_data['quantity']
            room_type = form.cleaned_data['room_type']
            additionals = form.cleaned_data['additional']
            entry_promo = form.cleaned_data['discount']

            day = date_leave - date_entry
            price = room_type.price * day.days
            # exist_promo = Promo.objects.get(name__contains=entry_promo)
            # if str(exist_promo) == entry_promo

            # print(str(exist_promo) == entry_promo)

            booking_info = {
                'pib': pib,
                'phone': phone,
                'email': email,
                'date_entry': date_entry,
                'date_leave': date_leave,
                'quantity': quantity,
                'room_type': room_type,
                'additionals': additionals,
                'days': day.days,
                'price': price
            }

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
                booking_status['fail'] = True
            else:
                booking = form.save(commit=False)
                booking.save()
                booking_status['success'] = True
        else:
            BookingForm()

    ctx = {
        'form': BookingForm,
        'booking_status': booking_status,
        'booking_info': booking_info
    }

    return render(request, 'form.html', ctx)


def contact(request):
    ctx={}
    return render(request, 'contacts.html', ctx)