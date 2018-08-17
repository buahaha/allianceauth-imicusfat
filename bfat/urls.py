from django.conf.urls import url

from . import views

app_name = 'bfat'

urlpatterns = [
    url(r'^$', views.bfat_view, name='bfat_view'),
    url(r'^stats/$', views.stats, name='stats'),
    url(r'^links/$', views.links, name='links'),
    url(r'^links/add/$', views.link_add, name='link_add')
]