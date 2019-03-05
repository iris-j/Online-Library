from django.db import models
from reader.models import Reader
from book.models import Book
import django.utils.timezone as timezone


class Comment(models.Model):

    user = models.ForeignKey(Reader, on_delete=models.CASCADE)
    isbn = models.ForeignKey(Book, on_delete=models.CASCADE)
    comment_time = models.DateTimeField(default=timezone.now)
    rating = models.IntegerField()
    content = models.CharField(max_length=150)


def _unicode_(self):
    return u'%s %s' % (self.user, self.isbn)

