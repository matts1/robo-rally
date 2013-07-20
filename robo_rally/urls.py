from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from robo_rally.auth.admin import *
admin.autodiscover()

from robo_rally.auth.views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'robo_rally.views.home', name='home'),
    # url(r'^robo_rally/', include('robo_rally.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^register/', RegisterView.as_view(), name='register')
)
