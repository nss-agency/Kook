"""Kook_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path, include
from core import views

urlpatterns = i18n_patterns(
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('hotel/', views.hotel, name='hotel'),
    path('contact/', views.contact, name='contact'),
    path('banquet/', views.banquet, name='banquet'),
    path('menu/', views.menu, name='menu'),
    path('restaurant/', views.restaurant, name='restaurant'),
    path('gallery/', views.gallery, name='gallery'),
    path('ajax_description/<id>', views.ajax_description, name='ajax_description'),
    path('pay/<id>', views.PayView.as_view(), name='pay_view'),
    path('pay-callback/<id>', views.PayCallbackView.as_view(), name='pay_callback'),
    path('ajax_second_step/', views.ajax_second_step, name='ajax_second_step'),
    prefix_default_language=False
)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

admin.site.site_header = "KOOK Адмін Панель"
admin.site.site_title = "Kook"
admin.site.index_title = "KOOK Адмін Панель"
