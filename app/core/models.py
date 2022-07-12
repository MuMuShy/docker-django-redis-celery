from django.db import models

# Create your models here.
class test(models.Model):
    name = models.CharField("姓名",max_length=10)