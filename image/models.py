#from django.db import models
from djongo import models

# Create your models here.


class Image(models.Model):
    image = models.ImageField(upload_to = 'images/',default=None)