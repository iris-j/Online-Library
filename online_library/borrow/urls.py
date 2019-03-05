from django.conf.urls import url
from borrow.views import easy_borrow, easy_return, renew


urlpatterns = [
    url(r'^easyborrow/(?P<isbn>\d+)/$', easy_borrow, name='easy_borrow'),
    url(r'^easyreturn/(?P<isbn>\d+)/$', easy_return, name='easy_return'),
    url(r'^renew/(?P<isbn>\d+)/$', renew, name='renew'),
]
