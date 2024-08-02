# Generated by Django 5.0.4 on 2024-07-23 18:50

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='actor',
            old_name='is_award',
            new_name='is_awarded',
        ),
        migrations.RenameField(
            model_name='movie',
            old_name='is_award',
            new_name='is_awarded',
        ),
        migrations.AlterField(
            model_name='director',
            name='years_of_experience',
            field=models.SmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]