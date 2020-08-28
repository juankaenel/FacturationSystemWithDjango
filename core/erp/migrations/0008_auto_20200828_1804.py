# Generated by Django 3.0.8 on 2020-08-28 21:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0007_auto_20200826_0117'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='birth_date',
        ),
        migrations.RemoveField(
            model_name='client',
            name='direction',
        ),
        migrations.RemoveField(
            model_name='client',
            name='last_names',
        ),
        migrations.RemoveField(
            model_name='client',
            name='sex',
        ),
        migrations.AddField(
            model_name='client',
            name='address',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Dirección'),
        ),
        migrations.AddField(
            model_name='client',
            name='date_birthday',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='Fecha de nacimiento'),
        ),
        migrations.AddField(
            model_name='client',
            name='gender',
            field=models.CharField(choices=[('male', 'Masculino'), ('female', 'Femenino')], default='male', max_length=12, verbose_name='Sexo'),
        ),
        migrations.AddField(
            model_name='client',
            name='surnames',
            field=models.CharField(default=1, max_length=150, verbose_name='Apellidos'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='client',
            name='dni',
            field=models.IntegerField(unique=True, verbose_name='DNI'),
        ),
        migrations.AlterField(
            model_name='client',
            name='names',
            field=models.CharField(max_length=150, verbose_name='Nombres'),
        ),
    ]
