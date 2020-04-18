from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .forms import BookingForm, BanquetForm
from .models import Booking, RoomType, Promo, Banquet, MenuItem, MenuCategories, GalleryPhoto, GalleryCategory
from django.http import HttpResponse, HttpResponseRedirect
from .decorators import check_recaptcha
from datetime import datetime, date
from django.urls import reverse

import random
from Kook_project import settings

from liqpay.liqpay import LiqPay

from django.views.generic import TemplateView
from django.shortcuts import render
from django.http import HttpResponse

from django.core.mail import send_mail, BadHeaderError


def send_contact(request):
    fname = request.POST.get('first_name', '')
    lname = request.POST.get('last_name', '')
    subject = 'Повідомлення з веб сайту'
    message = request.POST.get('message', '')
    from_email = request.POST.get('email', '')
    messages = 'Ім\'я та Прізвище: {} {}  \nВід кого повідомлення: {}\nПовідомлення: \n{}\n\n\n\nНадіслано з ' \
               '<a href="https://kook.in.ua">kook.in.ua</a>'.format(
        fname, lname, from_email, message)
    send_mail(subject, messages, 'noreply@kook.in.ua', ['setit49344@ualmail.com'], fail_silently=False)


def booking_element(request):
    booking_status = {
        'success': False,
        'fail': False,
    }

    form = BookingForm(request.POST)
    if form.is_valid():
        date_entry = form.cleaned_data['date_entry']
        date_leave = form.cleaned_data['date_leave']
        room_type = form.cleaned_data['room_type']
        entry_promo = form.cleaned_data['discount']
        day = date_leave - date_entry
        price = room_type.price * day.days
        new_price = price

        if Promo.objects.filter(name=entry_promo):
            exist_promo = Promo.objects.get(name=entry_promo)
            if exist_promo.date_expired >= datetime.now().date():
                if entry_promo == str(exist_promo) and exist_promo.is_percentage == False:
                    new_price = price - exist_promo.discount
                elif entry_promo == str(exist_promo) and exist_promo.is_percentage:
                    new_price = price - (price * (exist_promo.discount / 100))
                else:
                    new_price = price

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
            return None
        else:
            booking = form.save(commit=False)
            booking.price = new_price
            booking.save()
            booking_status['success'] = True
            print('Vil`no')
            return booking.id
    else:
        BookingForm()


def index(request):
    booking_status = {}

    if request.method == 'POST':
        booking_id = booking_element(request)
        if booking_id != None:
            return HttpResponseRedirect(f'/pay/{booking_id}')

    ctx = {
        'form': BookingForm,
        'booking_status': booking_status,
    }
    return render(request, 'index.html', ctx)


def restaurant(request):
    menu_items = MenuItem.objects.all()
    random_choice = ()
    if len(menu_items) >= 3:
        random_choice = random.sample(list(menu_items), 3)

    booking_status = {}

    if request.method == 'POST':
        booking_element(request)

    ctx = {
        'menu_items': random_choice,
        'form': BookingForm,
        'booking_status': booking_status,
    }
    return render(request, 'restaurant.html', ctx)


def menu(request):
    menu_items = MenuItem.objects.all()
    menu_categories = MenuCategories.objects.all()

    ctx = {'menu_items': menu_items,
           'menu_categories': menu_categories}
    return render(request, 'menu.html', ctx)


def gallery(request):
    gallery_items = GalleryPhoto.objects.all()
    gallery_categories = GalleryCategory.objects.all()
    filter = request.GET.get('f', '')

    ctx = {'gallery_items': gallery_items,
           'gallery_categories': gallery_categories,
           'filter': filter}
    return render(request, 'gallery.html', ctx)


def hotel(request):
    booking_status = {}

    if request.method == 'POST':
        booking_id = booking_element(request)
        if booking_id != None:
            return HttpResponseRedirect(f'/pay/{booking_id}')

    ctx = {
        'form': BookingForm,
        'booking_status': booking_status,
    }

    return render(request, 'hotel_rooms.html', ctx)


def banquet(request):
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
    return render(request, 'banquet.html', ctx)


@check_recaptcha
def contact(request):
    booking_status = {}

    if request.method == 'POST':
        booking_id = booking_element(request)
        if booking_id != None:
            return HttpResponseRedirect(f'/pay/{booking_id}')
        if request.recaptcha_is_valid:
            send_contact(request)
            ctx['success'] = True
        else:
            ctx['fail'] = True

    ctx = {'success': False,
           'fail': False,
           'form': BookingForm,
           'booking_status': booking_status,
           }

    return render(request, 'contacts.html', ctx)


def ajax_description(request, id):
    room = RoomType.objects.get(pk=id)

    ctx = {'room': room}

    return render(request, 'ajax_icludes/ajax_room_description.html', ctx)


def ajax_second_step(request):
    date_start = date.fromisoformat(request.GET.get('date_start', None))
    date_end = date.fromisoformat(request.GET.get('date_end', None))
    room_type_id = request.GET.get('id', None)
    entry_promo = request.GET.get('promo', '')
    email = request.GET.get('email', None)
    days = (date_end - date_start).days
    room = RoomType.objects.get(pk=room_type_id)
    ppd = room.price
    price = days * ppd
    new_price = price
    discount_value = 0
    if Promo.objects.filter(name=entry_promo):
        exist_promo = Promo.objects.get(name=entry_promo)
        if exist_promo.date_expired >= datetime.now().date():
            if entry_promo == str(exist_promo) and exist_promo.is_percentage is False:
                discount_value = exist_promo.discount
                new_price = price - discount_value
            elif entry_promo == str(exist_promo) and exist_promo.is_percentage:
                discount_value = (price * (exist_promo.discount / 100))
                new_price = price - discount_value
            else:
                new_price = price

    ctx = {'price': new_price,
           'old_price': price,
           'discount_value': discount_value,
           'days': days,
           'date_start': date_start,
           'date_end': date_end,
           'email': email,
           'room': room}

    return render(request, 'ajax_icludes/ajax_form_second_step_overview.html', ctx)


class PayView(TemplateView):
    template_name = 'pay.html'

    def get(self, request, id, *args, **kwargs):
        booking = Booking.objects.get(pk=id)
        liq_pay = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_PRIVATE_KEY)
        params = {
            'action': 'pay',
            'amount': booking.price,
            'currency': 'UAH',
            'description': 'Оплата за проживання {}'.format(booking.pib),
            'order_id': booking.id,
            'version': '3',
            'sandbox': 1,  # sandbox mode, set to 1 to enable it
            'server_url': 'http://127.0.0.1:8000/pay-callback/{}'.format(booking.id),  # url to callback view
        }
        signature = liq_pay.cnb_signature(params)
        data = liq_pay.cnb_data(params)
        return render(request, self.template_name, {'signature': signature, 'data': data})


@method_decorator(csrf_exempt, name='dispatch')
class PayCallbackView(View):
    def post(self, request, id, *args, **kwargs):
        booking = Booking.objects.get(pk=id)
        liq_pay = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_PRIVATE_KEY)
        data = request.POST.get('data')
        signature = request.POST.get('signature')
        sign = liq_pay.str_to_sign(settings.LIQPAY_PRIVATE_KEY + data + settings.LIQPAY_PRIVATE_KEY)
        if sign == signature:
            booking.is_paid = True
            booking.save()
        response = liq_pay.decode_data_from_str(data)
        print('callback data', response)
        return HttpResponse()
