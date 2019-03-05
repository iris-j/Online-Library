from django.conf.urls import url
from reader.views import personal_info, reader_login, reader_register, reader_logout, change_personal_info, change_headimg, change_password, sendemail
from django.views.generic import TemplateView
urlpatterns = [

    url(r'^reader/personalinfo/$', personal_info, name='reader_personalinfo'),
    url(r'^reader/changeinfo/$', change_personal_info, name='change_personalinfo'),
    url(r'^reader/changeheadimg/$', change_headimg, name='change_headimg'),
    url(r'^reader/changepassword/$', change_password, name='change_password'),
    url(r'^reader/login/$', reader_login),
    url(r'^reader/register/$', reader_register),
    url(r'^reader/logout/$', reader_logout),
    url(r'^reader/forgotpassword/$', sendemail, name="sendemail")


]