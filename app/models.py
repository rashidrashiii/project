from django.db import models

# Create your models here.
class table(models.Model):
    username2 = models.CharField(max_length=30)
    firstn = models.CharField(max_length=10)
    secondn = models.EmailField(max_length=100)
    address = models.CharField(max_length=100)
