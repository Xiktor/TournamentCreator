# Generated by Django 4.0.5 on 2022-07-07 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_alter_player_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='name',
            field=models.CharField(max_length=100, null=True, unique=True, verbose_name='Nazwa'),
        ),
    ]
