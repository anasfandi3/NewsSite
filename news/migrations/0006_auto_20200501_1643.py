# Generated by Django 3.0.4 on 2020-05-01 13:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0005_auto_20200501_1452'),
    ]

    operations = [
        migrations.RenameField(
            model_name='news',
            old_name='delete_at',
            new_name='update_at',
        ),
    ]