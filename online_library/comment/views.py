from django.shortcuts import render
from comment.models import Comment
from reader.models import Reader
from book.models import Book
from comment.models import Comment
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import Permission, User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response

@login_required(login_url='/reader/login')
def create_comment(request, isbn):
    user = request.user
    try:
        reader = Reader.objects.get(account__username__exact=user.username)

    except:
        return HttpResponseRedirect('/reader/login')
    else:
        target = Book.objects.get(isbn__exact=isbn)
        comments = Comment.objects.filter(isbn=target)
        if request.POST:

            content = request.POST.get('content', None)
            rating = request.POST.get('rating', None)
            comment = Comment(user=reader, isbn=target, rating=rating, content=content)
            comment.save()
            return HttpResponseRedirect('/reader/personalinfo')
        return render_to_response('comment/createcomment.html', locals())


def view_comment(request, isbn):
    target = Book.objects.get(isbn__exact=isbn)

    comments = Comment.objects.filter(isbn=target)
    total_rating = 0
    num = 0
    for line in comments:
        total_rating = total_rating + line.rating
        num = num + 1
    avg_rating = total_rating / num

    return render_to_response("comment/viewcomment.html", locals())


def delete_comment(request, comment_id):
    comment = Comment.objects.filter(id=comment_id)
    comment.delete()
    return HttpResponseRedirect('/reader/personalinfo')