from reader.models import Reader
from book.models import Book
from borrow.models import Borrow
from comment.models import Comment
from django.contrib.auth.models import Permission, User
from django.contrib.auth.decorators import user_passes_test, login_required
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.http import HttpResponse,HttpResponseRedirect
from django.core.files.base import ContentFile
import json
from django.contrib import auth
from random import choice
import string
from django.core.mail import send_mail

from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth import authenticate, login, logout



def reader_login(request):

    if request.method == 'POST':

            username = request.POST.get('username', None)
            password = request.POST.get('password', None)
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)  # login（request，User），就相当于设置了cookie和session
                return render_to_response('book/index.html')

            else:
                return HttpResponse('用户名或密码错误,请重新登录')

    return render_to_response('reader/readerlogin.html')


def reader_register(request):


    if request.method == 'POST':
            username = request.POST.get('username', None)
            password = request.POST.get('password', None)
            repeatpassword = request.POST.get('repeatpassword', None)
            nickname = request.POST.get('nickname', None)
            sex = request.POST.get('sex', None)
            phone = request.POST.get('phone', None)
            email = request.POST.get('email', None)
            file_content = ContentFile(request.FILES['icon'].read())
            # ImageField的save方法，第一个参数是保存的文件名，第二个参数是ContentFile对象，里面的内容是要上传的图片、视频的二进制内容


            if password == '' or repeatpassword == '':
                return HttpResponse('empty password')
            elif password != repeatpassword:
                return HttpResponse('repeat error')
            elif User.objects.filter(username=username):
                return HttpResponse('user exist')
            else:
                new_user = User.objects.create_user(username=username, password=password)
                new_user.save()
                new_reader = Reader(account=new_user, nickname=nickname,
                                    sex=sex, phone=phone, email=email)
                new_reader.save()
                new_reader.icon.save(request.FILES['icon'].name, file_content)
                return HttpResponseRedirect('/reader/login')

    return render_to_response('reader/readerregister.html')

def reader_logout(request):

    logout(request)

    return HttpResponseRedirect('/book/index')



@login_required(login_url='/reader/login/')
def personal_info(request):
    user = request.user
    try:
        reader = Reader.objects.get(account__username__exact=user.username)

    except:
        return HttpResponseRedirect('/reader/login')
    else:
        record = Borrow.objects.filter(user=reader)
        isbnlist = set()
        for item in record:
            isbnlist.add(item.isbn.isbn)
        booklist = Book.objects.filter(isbn__in=isbnlist)
        mycomments = Comment.objects.filter(user=reader)
        return render_to_response('reader/personalinfo.html', locals())

@login_required(login_url='/reader/login/')
def change_personal_info(request):
    user = request.user
    try:
        reader = Reader.objects.get(account__username__exact=user.username)

    except:
        return HttpResponseRedirect('/reader/login')
    else:
        if request.POST:
            reader.nickname = request.POST.get('nickname', None)
            reader.phone = request.POST.get('phone', None)
            reader.email = request.POST.get('email', None)

            reader.save()

            return HttpResponseRedirect('/reader/personalinfo')
        return render_to_response('reader/changepersonalinfo.html', locals())

@login_required(login_url='/reader/login/')
def change_headimg(request):
    user = request.user
    try:
        reader = Reader.objects.get(account__username__exact=user.username)

    except:
        return HttpResponseRedirect('/reader/login')
    else:
        if request.POST:
            file_content = ContentFile(request.FILES['newicon'].read())
            reader.icon.save(request.FILES['newicon'].name, file_content)
            return HttpResponseRedirect('/reader/personalinfo')
    return render_to_response('reader/changeheadimg.html', locals())

@login_required(login_url='/reader/login')
def change_password(request):
    user = request.user
    try:
        reader = Reader.objects.get(account__username__exact=user.username)

    except:
        return HttpResponseRedirect('/reader/login')
    else:
        if request.POST:
            origin = request.POST.get('origin', None)
            newpassword = request.POST.get('newpassword', None)
            repeatpassword = request.POST.get('repeatpassword', None)
            this_user = authenticate(username=user.username, password=origin)
            if this_user is not None:
                    if newpassword == repeatpassword:
                        this_user.set_password(newpassword)
                        this_user.save()
                        return HttpResponseRedirect('/reader/personalinfo')
                    else:
                        return HttpResponse('repeat error!')
            else:
                return HttpResponse('wrong password!')
    return render_to_response('reader/changepassword.html', locals())


def GenPassword(length=8, chars=string.ascii_letters + string.digits):
    return ''.join([choice(chars) for i in range(length)])

def sendemail(request):
    if request.POST:
        username = request.POST.get('username', None)
        try:
            user = User.objects.get(username=username)
            reader = Reader.objects.get(account=user)
        except:
            return HttpResponse('User not exist')
        else:
            emailaddress = reader.email
            pawdtemp = GenPassword(8)
            user.set_password(pawdtemp)
            user.save()

            send_mail(
                subject=u"这是新的密码,请使用新的密码登录", message=pawdtemp,
                from_email='1342640516@qq.com', recipient_list=[emailaddress, ], fail_silently=False,)
            return HttpResponse('新密码已经发送')
    return render_to_response('reader/forgotpassword.html')
