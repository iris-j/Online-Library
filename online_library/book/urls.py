from django.conf.urls import url
from book.views import showbook
from django.views.generic import TemplateView
urlpatterns = [

    url(r'^book/index/$', TemplateView.as_view(template_name="book/index.html")),
    url(r'^book/(?P<category>[A-Za-z]+)/$', showbook, name='show_book'),

]
