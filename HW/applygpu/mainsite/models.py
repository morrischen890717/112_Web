from django.db import models
from django.utils import timezone
# Create your models here.

class News(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, primary_key=True)
    body = models.TextField()
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('-date',)
    
    def __str__(self):
        return self.title