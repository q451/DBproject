from django.db import models

# Create your models here.

class user_account(models.Model):
    gender = (
        ('male', '男'),
        ('female', '女'),
    )

    username = models.CharField(max_length=128)
    password = models.CharField(max_length=128)
    phone = models.CharField(max_length=128, unique=True)
    email = models.EmailField(unique=True)

    time_created = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    birthday = models.DateField(null=True)
    sex = models.CharField(max_length=128, choices=gender, default='男')
    photo = models.ImageField(upload_to='png/')
    introduction = models.TextField(max_length=128)

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['time_created']
        verbose_name = '用户'
        verbose_name_plural = '用户'

class up_user(models.Model):
    username = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=128)
    email = models.EmailField(unique=True)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['time_created']
        verbose_name = '超级用户'
        verbose_name_plural = '超级用户'