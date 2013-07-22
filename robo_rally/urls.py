from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from robo_rally.auth.admin import *
admin.autodiscover()

from robo_rally.auth.views import *

urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    ### AUTH MODULE ###
    # in the login page, next page is provided by a hidden input field in the template
    url(r'^$', 'django.contrib.auth.views.login',
        dict(template_name='auth/login.html'), name='login'
    ),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
        dict(next_page= '/'), name='logout'
    ),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^chgpwd/$', ChgPwdView.as_view(), name='chgpwd'),
    url(r'^resetpwd/$', 'django.contrib.auth.views.password_reset',
        dict(template_name='auth/resetpwd.html', post_reset_redirect='/'), name='resetpwd'
    ),
    url(r'^resetpwd/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        'django.contrib.auth.views.password_reset_confirm',
        {'post_reset_redirect' : '/resetpwd/complete/'}
    ),

    ### GAME MODULE ###
    # TODO: registerView is a temporary view so I can get redirects working
    url(r'^lobbies/$', RegisterView.as_view(), name='lobbies'),
)
