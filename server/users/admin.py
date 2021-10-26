from django.contrib import admin
from . import models
# Register your models here.

# 把建的表放在admin里面可以页面管理

admin.site.register(models.user_account)
admin.site.register(models.up_user)
