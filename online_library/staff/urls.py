from django.conf.urls import url
from staff.views import staff_login, staff_relogin, staff_register, addBook, editBook, delBook, manageindex, manage_reader, delreader
urlpatterns = [

 #   url(r'^staff/personalinfo/$', personal_info, name='reader_personalinfo'),


    url(r'^staff/login/$', staff_login),
    url(r'^staff/relogin/$', staff_relogin),
    url(r'^staff/register/$', staff_register),
    url(r'^staff/addbook/$', addBook, name="books_add"),
    url(r'^staff/editbook/(?P<isbn>\d+)/$', editBook, name="books_edit"),
    url(r'^staff/delbook/(?P<isbn>\d+)/$', delBook, name="books_delete"),
    url(r'^staff/manage/book$', manageindex),
    url(r'^staff/manage/reader$', manage_reader),
    url(r'^staff/delreader/(?P<username>[_A-Za-z0-9]+)/$', delreader),


]