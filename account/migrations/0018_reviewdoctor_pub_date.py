# Generated by Django 4.1.3 on 2022-11-14 21:16

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0017_rename_review_reviewdoctor'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviewdoctor',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
