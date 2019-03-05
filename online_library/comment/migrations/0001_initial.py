# Generated by Django 2.0.4 on 2018-05-12 01:21

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('reader', '0001_initial'),
        ('book', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('rating', models.IntegerField()),
                ('content', models.CharField(max_length=150)),
                ('isbn', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.Book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reader.Reader')),
            ],
        ),
    ]
