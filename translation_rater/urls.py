from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import RedirectView

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^rater/', include('rater.urls', namespace="rater")),
    url(r'^$', RedirectView.as_view(url='/rater/')),
]
