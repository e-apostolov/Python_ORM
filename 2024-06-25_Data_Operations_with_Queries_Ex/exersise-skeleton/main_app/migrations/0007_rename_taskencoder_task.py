# Generated by Django 5.0.4 on 2024-06-29 14:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0006_taskencoder'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TaskEncoder',
            new_name='Task',
        ),
    ]