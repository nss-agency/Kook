from django.shortcuts import render, redirect
from .forms import BookingForm, BanquetForm
from .models import Booking, RoomType, Promo, Banquet
from .decorators import check_recaptcha
import datetime
from datetime import datetime


def index(request):
    ctx = {}
    return render(request, 'index.html', ctx)


def hotel(request):
    booking_status = {
        'success': False,
        'fail': False,
    }
    booking_info = {}
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            pib = form.cleaned_data['pib']
            phone = form.cleaned_data['phone']
            email = form.cleaned_data['email']
            date_entry = form.cleaned_data['date_entry']
            date_leave = form.cleaned_data['date_leave']
            quantity = form.cleaned_data['quantity']
            room_type = form.cleaned_data['room_type']
            additionals = form.cleaned_data['additional']
            entry_promo = form.cleaned_data['discount']
            day = date_leave - date_entry
            price = room_type.price * day.days
            new_price = price

            if Promo.objects.filter(name=entry_promo):
                exist_promo = Promo.objects.get(name=entry_promo)
                if entry_promo == str(exist_promo) and exist_promo.is_percetage == False:
                    new_price = price - exist_promo.discount
                elif entry_promo == str(exist_promo) and exist_promo.is_percetage:
                    new_price = price - (price * (exist_promo.discount / 100))
                else:
                    new_price = price

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
        'booking_status': booking_status
    }
    return render(request, 'hotel_rooms.html', ctx)


def banquet(request):
    ctx = {}
    return render(request, 'banquet.html', ctx)


def form(request):
    booking_status = {
        'success': False,
        'fail': False,
    }

    booking_info = {}
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            pib = form.cleaned_data['pib']
            phone = form.cleaned_data['phone']
            email = form.cleaned_data['email']
            date_entry = form.cleaned_data['date_entry']
            date_leave = form.cleaned_data['date_leave']
            quantity = form.cleaned_data['quantity']
            room_type = form.cleaned_data['room_type']
            additionals = form.cleaned_data['additional']
            entry_promo = form.cleaned_data['discount']
            day = date_leave - date_entry
            price = room_type.price * day.days
            new_price = price


            if Promo.objects.filter(name=entry_promo):
                exist_promo = Promo.objects.get(name=entry_promo)
                if exist_promo.date_expired > datetime.now().date():
                    if entry_promo == str(exist_promo) and exist_promo.is_percentage == False:
                        new_price = price - exist_promo.discount
                    elif entry_promo == str(exist_promo) and exist_promo.is_percentage:
                        new_price = price - (price * (exist_promo.discount / 100))
                    else:
                        new_price = price

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
                'price': new_price
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
    ctx = {}
    return render(request, 'contacts.html', ctx)


def banquet_form(request):
    banquet_status = {
        'success': False,
        'fail': False,
    }

    if request.method == 'POST':
        form = BanquetForm(request.POST)
        if form.is_valid():
            check_in = form.cleaned_data['check_in']
            case = Banquet.objects.filter(check_in=check_in).exists()

            if case:
                print('Zanyato')
                banquet_status['fail'] = True
            else:
                banquet = form.save(commit=False)
                banquet.save()
                banquet_status['success'] = True
        else:
            BanquetForm()

    ctx = {
        'form': BanquetForm,
        'banquet_status': banquet_status,
    }
    return render(request, 'banque_form.html', ctx)
