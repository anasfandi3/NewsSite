# Generated by Django 3.0.4 on 2020-05-20 20:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0008_auto_20200519_1845'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='parent',
        ),
    ]
