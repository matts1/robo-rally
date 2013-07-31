from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView
from django.contrib.auth.forms import SetPasswordForm

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from robo_rally.auth.admin import * # create admin view

admin.autodiscover()

from robo_rally.auth.views import *
from robo_rally.courses.views import *
from robo_rally.game.views import *

urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^showmsg/(?P<msg>.+)/(?P<redirect>.+)', MsgView.as_view(), name='msg'),

    # favicon
    url(r'^favicon.ico$', RedirectView.as_view(url='/static/images/favicon.ico')),

    ### AUTH MODULE ###
    # in the login page, next page is provided by a hidden input field in the template
    url(r'^$', 'django.contrib.auth.views.login',
        dict(template_name='auth/login.html'), name='login'
    ),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
        dict(next_page= '/'), name='logout'
    ),
    url(r'^resetpwd/$', ResetPwdView.as_view(), name='resetpwd'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^chgpwd/$', ChgPwdView.as_view(), name='chgpwd'),

    url(r'^resetpwd/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        'django.contrib.auth.views.password_reset_confirm',
        dict(
            template_name='auth/resetpwd.html',
            post_reset_redirect=reverse_lazy(
                'msg', kwargs=dict(msg='doreset', redirect='login')),
            set_password_form=SetPasswordForm
        ), name='doreset'
    ),
    url('^resetpwd/doreset/$', 'django.contrib.auth.views.password_reset_complete', name='completereset'),

    ### GAME MODULE ###
    # TODO: registerView is a temporary view so I can test getting redirects working
    url(r'^lobbies/$', RegisterView.as_view(), name='lobbies'),
    url(r'^pickmap/$', PickMapView.as_view(), name='maplist'),
    url(r'^courses/(?P<url>.+)$', ViewCourseView.as_view(), name='course'),
)
