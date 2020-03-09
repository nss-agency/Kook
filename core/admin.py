from django.contrib import admin
from .models import Booking, MenuItem, RoomType


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
    list_filter = ['date_entry', 'date_leave']
    search_fields = ['phone']


admin.site.register(Booking, BookingAdmin)
admin.site.register(MenuItem)
admin.site.register(RoomType)
