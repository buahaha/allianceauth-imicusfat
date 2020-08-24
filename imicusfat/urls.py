from django.conf.urls import url

from . import views


app_name = "imicusfat"

urlpatterns = [
    url(r"^$", views.imicusfat_view, name="imicusfat_view"),
    url(r"^stats/$", views.stats, name="stats"),
    url(r"^stats/corp/$", views.stats_corp, name="stats_corp"),
    url(r"^stats/corp/(?P<corpid>[0-9]+)/$", views.stats_corp, name="stats_corp"),
    url(
        r"^stats/corp/(?P<corpid>[0-9]+)/(?P<month>[0-9]+)/(?P<year>[0-9]+)/$",
        views.stats_corp,
        name="stats_corp",
    ),
    url(r"^stats/char/$", views.stats_char, name="stats_char"),
    url(r"^stats/char/(?P<charid>[0-9]+)/$", views.stats_char, name="stats_char"),
    url(
        r"^stats/char/(?P<charid>[0-9]+)/(?P<month>[0-9]+)/(?P<year>[0-9]+)/$",
        views.stats_char,
        name="stats_char",
    ),
    url(r"^stats/ally/$", views.stats_alliance, name="stats_ally"),
    url(
        r"^stats/ally/(?P<allianceid>[0-9]+)/$", views.stats_alliance, name="stats_ally"
    ),
    url(
        r"^stats/ally/(?P<allianceid>[0-9]+)/(?P<month>[0-9]+)/(?P<year>[0-9]+)/$",
        views.stats_alliance,
        name="stats_ally",
    ),
    url(r"^links/$", views.links, name="links"),
    url(
        r"^links/create/esi/(?P<hash>[a-zA-Z0-9]+)/$",
        views.link_create_esi,
        name="link_create_esi",
    ),
    url(r"^links/create/esifat/$", views.create_esi_fat, name="create_esi_fat"),
    url(r"^links/create/click/$", views.link_create_click, name="link_create_click"),
    url(r"^links/add/$", views.link_add, name="link_add"),
    url(r"^links/edit/$", views.edit_link, name="link_edit"),
    url(r"^links/(?P<hash>[a-zA-Z0-9]+)/edit/$", views.edit_link, name="link_edit"),
    url(r"^links/(?P<hash>[a-zA-Z0-9]+)/click/$", views.click_link, name="link_click"),
    url(r"^links/del/$", views.del_link, name="link_delete"),
    url(r"^links/(?P<hash>[a-zA-Z0-9]+)/del/$", views.del_link, name="link_delete"),
    url(
        r"^links/(?P<hash>[a-zA-Z0-9]+)/(?P<fat>[0-9]+)/del/$",
        views.del_fat,
        name="fat_delete",
    ),
]
