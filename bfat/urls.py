from django.conf.urls import url

from . import views

app_name = 'bfat'

urlpatterns = [
    url(r'^$', views.bfat_view, name='bfat_view'),
    url(r'^stats', views.bfat_stats, name='bfat_stats'),
]