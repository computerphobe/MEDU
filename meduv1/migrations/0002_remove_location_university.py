# Generated by Django 3.1.13 on 2025-02-27 07:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meduv1', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='university',
        ),
    ]
