# Generated by Django 3.0.4 on 2020-06-05 05:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0021_news_testfield'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='testfield',
        ),
    ]
