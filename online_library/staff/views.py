from staff.models import Staff
from book.models import Book
from reader.models import Reader
from borrow.models import Borrow
from comment.models import Comment
from django.contrib.auth.models import Permission, User
from django.contrib.auth.decorators import user_passes_test, login_required, permission_required
from django.http import HttpResponse,HttpResponseRedirect
import json
from django.contrib import auth

from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth import authenticate, login, logout

def staff_login(request):

    if request.method == 'POST':

            username = request.POST.get('username', None)
            password = request.POST.get('password', None)
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)  # login（request，User），就相当于设置了cookie和session
                return HttpResponseRedirect('/staff/manage/book')

            else:
                return HttpResponseRedirect('/staff/relogin')

    return render_to_response('staff/stafflogin.html')

def staff_relogin(request):
    return render_to_response('staff/relogin.html')

def staff_register(request):


    if request.method == 'POST':
            username = request.POST.get('username', None)
            password = request.POST.get('password', None)
            repeatpassword = request.POST.get('repeatpassword', None)
            firstname = request.POST.get('firstname', None)
            lastname = request.POST.get('lastname', None)
            sex = request.POST.get('sex', None)
            phone = request.POST.get('phone', None)
            email = request.POST.get('email', None)
            if password == '' or repeatpassword == '':
                return HttpResponse('empty password')
            elif password != repeatpassword:
                return HttpResponse('repeat error')
            elif User.objects.filter(username=username):
                return HttpResponse('user exist')
            else:
                new_user = User.objects.create_user(username=username, password=password)
                new_user.save()
                new_staff = Staff(account=new_user, firstname=firstname,
                                  lastname=lastname, sex=sex, phone=phone, email=email)
                new_staff.save()
                return HttpResponseRedirect('/staff/login')

    return render_to_response('staff/staffregister.html')


@login_required(login_url='/staff/login')
def manageindex(request):
    user = request.user
    try:
        staff = Staff.objects.get(account__username__exact=user.username)
    except:
        return HttpResponseRedirect('/staff/login')
    else:
        books = Book.objects.all()
        return render_to_response('staff/bookmanage1.html', locals())




@login_required(login_url='/staff/login')
def manage_reader(request):
    user = request.user
    try:
        staff = Staff.objects.get(account__username__exact=user.username)
    except:
        return HttpResponseRedirect('/staff/login')
    else:
        readers = Reader.objects.all()
    return render_to_response('staff/readermanage.html', locals())


@login_required(login_url='/staff/login/')
def addBook(request):  # request method 确定与服务器交互的方法，GET一般用于获取/查询资源信息，POST一般用于更新资源信息
    user = request.user
    try:
        staff = Staff.objects.get(account__username__exact=user.username)
    except:
        return HttpResponse('Permission denied')
    else:
        if request.POST:

            isbn = request.POST.get('isbn', None)
            title = request.POST.get('title', None)
            author = request.POST.get('author', None)
            publisher = request.POST.get('publisher', None)
            details = request.POST.get('douban link', None)
            category = request.POST.get('category', None)
            quantity = request.POST.get('quantity', None)
            remain = request.POST.get('remain', None)
            isbns = Book.objects.filter(isbn__exact=isbn)
            if isbns:
                resp1 = {'info': 'Already exists!', 'result': 'Already exists!'}
                return HttpResponse(json.dumps(resp1), content_type="application/json")
            else:
                book = Book(isbn=isbn, title=title, author=author, publisher=publisher,
                            details=details, category=category, quantity=quantity, remain=remain)
                book.save()

                return HttpResponseRedirect('/staff/manage')

        return render_to_response('book/add.html')

@login_required(login_url='/staff/login/')
def editBook(request,isbn):
    user = request.user
    try:
        staff = Staff.objects.get(account__username__exact=user.username)
    except:
        return HttpResponse('Permission denied')
    else:
        book = get_object_or_404(Book, pk=int(isbn))  # pk 是主键吗？没有规定？
        if request.POST:
            book.isbn = request.POST.get('isbn', None)
            book.title = request.POST.get('title', None)
            book.author = request.POST.get('author', None)
            book.publisher = request.POST.get('publisher', None)
            book.details = request.POST.get('douban link', None)
            book.category = request.POST.get('category', None)
            book.quantity = request.POST.get('quantity', None)
            book.remain = request.POST.get('remain', None)
            book.save()
            return HttpResponseRedirect('/staff/manage')
        return render_to_response('book/edit.html', {'book': book})

@login_required(login_url='/staff/login/')
def delBook(request, isbn):
    user = request.user
    try:
        staff = Staff.objects.get(account__username__exact=user.username)
    except:
        return HttpResponse('Permission denied')
    else:
        book = Book.objects.get(isbn=isbn)
        book.delete()
        return HttpResponseRedirect('/staff/manage')

@login_required(login_url='/staff/login/')
def delreader(request, username):
    user = request.user
    try:
        staff = Staff.objects.get(account__username__exact=user.username)
    except:
        return HttpResponse('Permission denied')
    else:
        deluser = User.objects.get(username__exact=username)
        delreader = Reader.objects.get(account=deluser)
        delborrow = Borrow.objects.filter(user=delreader)
        delcomment = Comment.objects.filter(user=delreader)
        for line in delborrow:
            book = Book.objects.get(isbn__exact=line.isbn.isbn)
            book.remain = book.remain+1
            book.save()
            line.delete()
        for line in delcomment:
            line.delete()
        delreader.delete()
        deluser.delete()
    return HttpResponseRedirect('/staff/manage/reader')
