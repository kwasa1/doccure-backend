# Generated by Django 4.1.3 on 2022-11-17 04:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workingday',
            name='openning_time',
            field=models.TimeField(),
        ),
    ]
