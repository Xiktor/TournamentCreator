# Generated by Django 4.0.5 on 2022-07-08 01:22

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_delete_acc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournament',
            name='max_players',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(2), django.core.validators.MaxValueValidator(500)], verbose_name='Max graczy'),
        ),
    ]
