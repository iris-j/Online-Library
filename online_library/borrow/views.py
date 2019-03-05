from django.shortcuts import render
from book.models import Book
from borrow.models import Borrow
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import user_passes_test, login_required
from django.http import HttpResponse, HttpResponseRedirect
import json
import django.utils.timezone as timezone
import datetime
from reader.models import Reader

@login_required(login_url='/reader/login/')
def easy_borrow(request, isbn):
    target = get_object_or_404(Book, pk=int(isbn))
    if request.POST:
        username = request.user.username
        reader = Reader.objects.get(account__username__exact=username)
        if target:
            exist = Borrow.objects.filter(user=reader, isbn=target)
            if exist.exists():
                return HttpResponse('Already borrowed!')
            else:
                if target.remain > 0:
                    record = Borrow(user=reader, isbn=target)
                    record.save()
                    target.remain = target.remain - 1
                    target.save()
                    return HttpResponseRedirect('/reader/personalinfo')
                else:
                    return HttpResponse('No book remain')
        else:
            return HttpResponse('No such book')
    return render_to_response('borrow/easyborrow.html', {'book': target})




@login_required(login_url='/reader/login/')
def easy_return(request, isbn):
    target = Book.objects.get(isbn__exact=isbn)
    if request.POST:
        username = request.user.username

        reader = Reader.objects.get(account__username__exact=username)
        if target:
            record = Borrow.objects.get(user__exact=reader,
                                        isbn__exact=target.isbn)
            if record:
                returntime = timezone.now()
                if returntime > record.due_time:
                    record.delete()
                    target.remain = target.remain + 1
                    target.save()
                    return HttpResponse('Return book latency')
                else:
                    record.delete()
                    target.remain = target.remain + 1
                    target.save()
                    return HttpResponseRedirect('/reader/personalinfo')
            else:
                return HttpResponse('No such borrow record')
        else:
            return HttpResponse('No such book')
    return render_to_response('borrow/easyreturn.html', {'book': target})


def renew(request, isbn):
    target = Book.objects.get(isbn__exact=isbn)
    if request.POST:
        username = request.user.username
        reader = Reader.objects.get(account__username__exact=username)
        if target:
            record = Borrow.objects.get(user__exact=reader,
                                        isbn__exact=target.isbn)
            if record:
                if record.due_time > timezone.now():
                    record.due_time = record.due_time + datetime.timedelta(30)
                    record.save()
                    return HttpResponseRedirect('/reader/personalinfo')
                else:
                    return HttpResponse('This book is overdue, please pay the fine first! ')
            else:
                return HttpResponse('No such book record')
        else:
            return HttpResponse('No such book')
    return render_to_response('borrow/renew.html', locals())
