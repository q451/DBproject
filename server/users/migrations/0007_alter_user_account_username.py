# Generated by Django 3.2.5 on 2021-10-18 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_user_account_update_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_account',
            name='username',
            field=models.CharField(max_length=128),
        ),
    ]
