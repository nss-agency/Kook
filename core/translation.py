from modeltranslation.translator import register, TranslationOptions
from .models import *


@register(MenuCategories)
class PostTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(MenuItem)
class PostTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)


@register(RoomType)
class PostTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


@register(Slider)
class PostTranslationOptions(TranslationOptions):
    fields = ('title', 'sub_title')
