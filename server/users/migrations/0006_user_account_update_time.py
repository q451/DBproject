# Generated by Django 3.2.5 on 2021-10-17 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20211014_1526'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_account',
            name='update_time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
