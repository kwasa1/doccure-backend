# Generated by Django 4.1.3 on 2022-11-13 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_profile_bio_achievement'),
    ]

    operations = [
        migrations.AlterField(
            model_name='achievement',
            name='year',
            field=models.DateField(auto_now=True, null=True, verbose_name='Achievement Date'),
        ),
    ]
