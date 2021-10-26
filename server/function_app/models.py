from django.db import models

# Create your models here.
class test(models.Model):
    username = models.CharField(max_length=128)
    time_created = models.DateTimeField(auto_now_add=True)
    birthday = models.DateField(null=True)
    sex = models.CharField(max_length=128)
    age = models.IntegerField()

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['time_created']
        verbose_name = '测试专业数据库'
        verbose_name_plural = '测试专业数据库'


class photo(models.Model):
    username = models.CharField(max_length=128)
    time_created = models.DateTimeField(auto_now_add=True)
    picture = models.ImageField()

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['time_created']
        verbose_name = '头像数据库测试'
        verbose_name_plural = '头像数据库测试'

class movie(models.Model):
    url_link = models.TextField(max_length=256)
    photo_link = models.TextField(max_length=256)
    chinese_name = models.TextField(max_length=256)
    origin_name = models.TextField(max_length=256)
    score = models.FloatField(max_length=256)
    rated = models.TextField(max_length=256)
    introduction = models.TextField(max_length=256)
    actors = models.TextField(max_length=256)

    def __str__(self):
        return self.chinese_name

    class Meta:
        verbose_name = '豆瓣电影前250'
        verbose_name_plural = '爬虫获取数据'