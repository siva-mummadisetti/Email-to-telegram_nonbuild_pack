# Generated by Django 3.2.2 on 2021-10-18 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Email', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usrdata',
            name='email_password',
            field=models.TextField(blank=True),
        ),
    ]
