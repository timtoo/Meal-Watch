# ROOT_URL_CONF file for stand-alone dev/testing
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    (r'^dinner/', include('dinner.urls')),
)
