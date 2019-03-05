from django.conf.urls import url
from comment.views import create_comment, view_comment, delete_comment


urlpatterns = [
    url(r'^comment/create/(?P<isbn>\d+)/$', create_comment, name='create_comment'),
    url(r'^comment/view/(?P<isbn>\d+)/$', view_comment, name='view_comment'),
    url(r'^comment/delete/(?P<comment_id>\d+)/$', delete_comment, name='delete_comment'),
]
