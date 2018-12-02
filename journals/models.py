from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.
#TODO TODO TODO create unique slugs for users!!!
class Journal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    body = models.TextField()
    date = models.DateTimeField(default=now)
    public = models.BooleanField(default=False)
