# Generated by Django 3.2.2 on 2021-10-21 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Email', '0006_auto_20211019_1956'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='reqCount',
            field=models.IntegerField(default=0),
        ),
    ]
