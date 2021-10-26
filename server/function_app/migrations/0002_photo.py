# Generated by Django 3.2.5 on 2021-10-22 00:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('function_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=128)),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('picture', models.ImageField(upload_to='')),
            ],
            options={
                'verbose_name': '头像数据库测试',
                'verbose_name_plural': '头像数据库测试',
                'ordering': ['time_created'],
            },
        ),
    ]
