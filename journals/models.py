from django.db import models
from tinymce import models as tinymce_models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.

class Journal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    body = tinymce_models.HTMLField()
    date = models.DateTimeField(default=now)
    public = models.BooleanField(default=False)
