# Generated by Django 3.2.2 on 2021-10-18 15:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Email', '0002_alter_usrdata_email_password'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]