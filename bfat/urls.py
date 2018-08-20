from django.conf.urls import url

from . import views

app_name = 'bfat'

urlpatterns = [
    url(r'^$', views.bfat_view, name='bfat_view'),
    url(r'^stats/$', views.stats, name='stats'),
    url(r'^links/$', views.links, name='links'),
    url(r'^links/(?P<page>[0-9]+)/$', views.links, name='links'),
    url(r'^links/add/$', views.link_add, name='link_add'),
    url(r'^links/edit/$', views.edit_link, name="link_edit"),
    url(r'^links/(?P<hash>[a-zA-Z0-9]+)/edit/$', views.edit_link, name="link_edit"),
    url(r'^links/del/$', views.del_link, name="link_delete"),
    url(r'^links/(?P<hash>[a-zA-Z0-9]+)/del/$', views.del_link, name="link_delete"),
    url(r'^links/(?P<hash>[a-zA-Z0-9]+)/(?P<fat>[0-9]+)/del/$', views.del_fat, name="link_delete"),
]