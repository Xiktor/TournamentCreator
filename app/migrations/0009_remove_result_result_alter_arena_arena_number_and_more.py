# Generated by Django 4.0.5 on 2022-07-06 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_remove_arena_result_remove_arena_winner_result'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='result',
            name='result',
        ),
        migrations.AlterField(
            model_name='arena',
            name='arena_number',
            field=models.IntegerField(null=True, verbose_name='Stolik nr'),
        ),
        migrations.AlterField(
            model_name='player',
            name='name',
            field=models.CharField(max_length=100, null=True, verbose_name='Nazwa'),
        ),
        migrations.AlterField(
            model_name='round',
            name='round_number',
            field=models.IntegerField(null=True, verbose_name='Runda nr'),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='is_finished',
            field=models.BooleanField(default=False, verbose_name='Zakończony'),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='is_started',
            field=models.BooleanField(default=False, verbose_name='Rozpoczęty'),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='max_players',
            field=models.IntegerField(verbose_name='Max graczy'),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='name',
            field=models.CharField(max_length=100, null=True, verbose_name='Nazwa'),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='players',
            field=models.ManyToManyField(null=True, related_name='Gracze', to='app.player'),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='start_date',
            field=models.DateTimeField(null=True, verbose_name='Rozpoczęcie'),
        ),
    ]