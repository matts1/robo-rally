# coding: utf-8
from django.conf.urls import patterns, url, include
import robo_rally.messages.views as views

urlpatterns = patterns("",
    url(
        regex=r"^send/$",
        view=views.MessageCreateView.as_view(),
        name="realtime_message_create",
    ),
)
