from django.db import models

#  要创建的表必须是APP不然无法迁移！！


class Book(models.Model):
    isbn = models.CharField(max_length=50, primary_key=True, null=False)
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    publisher = models.CharField(max_length=50)
    details = models.URLField()
    category = models.CharField(max_length=50)
    quantity = models.IntegerField()
    remain = models.IntegerField()

    def _unicode_(self):
        return self.title
