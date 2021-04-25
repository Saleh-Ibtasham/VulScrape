from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class SourceCode(models.Model):
    files = models.TextField()

    def __str__(self):
        return self.id