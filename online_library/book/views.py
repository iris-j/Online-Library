from book.models import Book
from reader.models import Reader
from django.core.paginator import Paginator, InvalidPage, EmptyPage
#  django自带分页工具
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
import json
from django.template import RequestContext

def showbook(request, category):
    user = request.user
    try:
        reader = Reader.objects.get(account__username__exact=user.username)

    except:
        reader = None
    books = Book.objects.filter(category__exact=category)
    if books.exists():
        cate = books[0].category
    else:
        cate = ""
    return render_to_response('book/booklist.html', locals())

