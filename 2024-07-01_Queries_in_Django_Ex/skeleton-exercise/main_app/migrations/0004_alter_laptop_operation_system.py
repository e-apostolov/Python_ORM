# Generated by Django 5.0.4 on 2024-07-01 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_laptop'),
    ]

    operations = [
        migrations.AlterField(
            model_name='laptop',
            name='operation_system',
            field=models.CharField(choices=[('Windows', 'Windows'), ('MacOS', 'MacOS'), ('Linux', 'Linux'), ('Chrome OS', 'Chrome OS')], max_length=20),
        ),
    ]
