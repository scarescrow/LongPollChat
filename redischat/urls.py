from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^hello$', views.hello, name='hello'),
    url(r'^sendmessage$', views.sendMessage, name='send'),
    url(r'^getpendingmessages$', views.getPendingMessages, name='receive'),
    url(r'^startclient$', views.startClient, name='start'),
    url(r'^stopclient$', views.stopClient, name='stop'),
]