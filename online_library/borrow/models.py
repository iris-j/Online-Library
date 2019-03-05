from django.db import models
from book.models import Book
from reader.models import Reader
import django.utils.timezone as timezone
import datetime


def sixty_days_later():
    return timezone.now() + datetime.timedelta(60)


class Borrow(models.Model):

    user = models.ForeignKey(Reader, on_delete=models.CASCADE)
    isbn = models.ForeignKey(Book, on_delete=models.CASCADE)
    borr_time = models.DateTimeField(default=timezone.now)
    due_time = models.DateTimeField(default=sixty_days_later)
    class Meta:
        unique_together=("user", "isbn")


def _unicode_(self):
    return u'%s %s' % (self.user, self.isbn)



