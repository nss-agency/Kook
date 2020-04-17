from django.contrib import admin

from Kook_project.actions import export_as_csv_action
from .models import Booking, MenuItem, RoomType, Promo, Banquet, MenuCategories, GalleryCategory, GalleryPhoto
from modeltranslation.admin import TabbedTranslationAdmin


# class PhotoInline(admin.StackedInline):
#     model = Photo
#     extra = 1


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
        'additional',
        'discount',
        'price',
        'is_paid']
    list_filter = ['room_type', 'date_entry', 'date_leave']
    search_fields = ('phone', 'pib', 'email')
    list_per_page = 10
    date_hierarchy = 'date_entry'
    actions = [export_as_csv_action("Експорт обрані Замовлення в CSV", fields=list_display)]


class BanquetAdmin(admin.ModelAdmin):
    list_display = [
        'pib',
        'phone',
        'email',
        'check_in',
    ]
    list_filter = ['check_in']
    search_fields = ('phone', 'pib', 'email')
    list_per_page = 10
    date_hierarchy = 'check_in'


class RoomAdmin(TabbedTranslationAdmin):
    list_display = [
        'name',
        'quantity',
        'price',
    ]


class PromoAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'discount',
        'is_percentage',
    ]


class MenuCategoriesAdmin(TabbedTranslationAdmin):
    list_display = ['name']


class MenuItemAdmin(TabbedTranslationAdmin):
    search_fields = ('name',)
    list_display = ['title',
                    'price']


admin.site.register(Booking, BookingAdmin)
admin.site.register(MenuCategories, MenuCategoriesAdmin)
admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(Promo, PromoAdmin)
admin.site.register(Banquet, BanquetAdmin)
admin.site.register(RoomType, RoomAdmin)
admin.site.register(GalleryCategory)
admin.site.register(GalleryPhoto)
