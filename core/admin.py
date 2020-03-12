from django.contrib import admin
from .models import Booking, MenuItem, RoomType, Promo, Baquet


# Register your models here.

class BookingAdmin(admin.ModelAdmin):
    list_display = [
        'pib',
        'phone',
        'email',
        'date_entry',
        'date_leave',
        'quantity',
        'room_type',
        'additional']
    list_filter = ['room_type', 'date_entry', 'date_leave']
    search_fields = ('phone', 'pib', 'date_entry', 'date_leave', 'email')
    list_per_page = 10
    date_hierarchy = 'date_entry'


class RoomAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'quantity',
        'price',
    ]


admin.site.register(Booking, BookingAdmin)
admin.site.register(MenuItem)
admin.site.register(Promo)
admin.site.register(Baquet)
admin.site.register(RoomType, RoomAdmin)
