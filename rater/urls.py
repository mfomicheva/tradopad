from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^access/$', views.access, name='access'),
    url(r'^rate/$', views.rate, name='rate'),
    url(r'^finish/$', views.finish, name='finish'),
    url(r'^(?P<segment_id>[0-9]+)/submit_rating/$', views.submit_rating, name='submit_rating'),
]