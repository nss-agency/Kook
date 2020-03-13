from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_delete
from datetime import datetime
from core.google_calendar import create_event_from_booking, create_event_from_banquet
from django.conf import settings


class Promo(models.Model):
    """
    Model for promocodes
    """
    name = models.CharField('Код Промокоду', max_length=60)
    discount = models.FloatField('Значення промокоду')
    is_percetage = models.BooleanField('Це відсоток?', default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Промокод'
        verbose_name_plural = 'Промокоди'


class RoomType(models.Model):
    """
       Model for room types
    """
    image = models.ImageField('Фото кімнати', upload_to='room_types', blank=True)
    name = models.CharField('Тип Кімнати', max_length=64)
    quantity = models.IntegerField('Кількість кімнат')
    color_id = models.IntegerField('Id кольору')
    price = models.PositiveIntegerField('Ціна')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип Кімнати'
        verbose_name_plural = 'Типи Кімнат'


class Booking(models.Model):
    """
    Model for Booking
    """
    pib = models.CharField('П.І.Б.', max_length=225)
    phone = models.CharField('Номер телефону', max_length=225, help_text='Контактний номер телефону')
    email = models.EmailField('E-mail')
    date_entry = models.DateField('Дата заїзду', default=datetime.now)
    date_leave = models.DateField('Дата виїзду', default=datetime.now)
    quantity = models.IntegerField('Кількість осіб')
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    additional = models.CharField('Додаткові опціі', max_length=225)
    breakfest = models.BooleanField('Сніданок', default=True)
    bed_type = models.CharField('Тип Ліжка', null=True, blank=True, max_length=225)
    notes = models.TextField('Нотатки', blank=True, help_text='Цей текст буде бачити тільки адміністратор та модератор')
    is_paid = models.BooleanField(default=False)
    discount = models.CharField('Промокод', max_length=225, null=True, blank=True)

    # save event to google calendar
    def save(self, *args, **kwargs):
        super().save()
        if settings.ENABLE_GOOGLE_CALENDAR:
            create_event_from_booking(self)

    def __str__(self):
        template = '{0.pib} | {0.phone} | {0.room_type}'
        return template.format(self)

    class Meta:
        verbose_name = 'Замовлення'
        verbose_name_plural = 'Замовлення'


class MenuItem(models.Model):
    """
    Model for menu items
    """
    image = models.ImageField('Зображення', blank=True, upload_to='menu_images')
    title = models.CharField('Назва страви', max_length=225)
    description = models.TextField('Опис')
    price = models.IntegerField('Ціна')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукти'


class Baquet(models.Model):
    check_in = models.DateField('Заїзд', default=datetime.now)
    pib = models.CharField('П.І.Б.', max_length=225)
    phone = models.CharField('Номер телефону', max_length=225, help_text='Контактний номер телефону')
    email = models.EmailField('E-mail')
    notes = models.TextField('Нотатки', blank=True, help_text='Цей текст буде бачити тільки адміністратор та модератор')

    def save(self, *args, **kwargs):
        super().save()
        if settings.ENABLE_GOOGLE_CALENDAR:
            create_event_from_banquet(self)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Банкет'
        verbose_name_plural = 'Банкет'


# Delete photo if model.object delete
@receiver(post_delete)
def submission_delete(sender, instance, **kwargs):
    try:
        instance.image.delete(False)
    except AttributeError:
        pass
