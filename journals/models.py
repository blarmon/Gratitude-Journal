from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django_extensions.db.fields import AutoSlugField
from django.db.models.signals import post_save
from django.dispatch import receiver
from taggit.managers import TaggableManager

# Create your models here.
class Journal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    body = models.TextField()
    date = models.DateTimeField(default=now)
    public = models.BooleanField(default=False)
    slug = AutoSlugField(populate_from=['title'])
    tags = TaggableManager(blank=True)


class UserExtension(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = AutoSlugField(populate_from=['user__username'])
    follows = models.ManyToManyField('UserExtension', related_name='followed_by')
    user_image = models.ImageField(upload_to='journals/images/', default='journals/images/no-img.png', blank=True, null=True)

@receiver(post_save, sender=User)
def create_user_extension(sender, instance, created, **kwargs):
    if created:
        UserExtension.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_extension(sender, instance, **kwargs):
    instance.userextension.save()


# TODO helper function to return a blurb from the body of a journal.
# TODO maybe overwrite the save function to do this!  thats a pretty good idea...
# TODO make sure to write the test for the function before you start!!!
# TODO is there a way to base the blurb off of screen size?  probably not.  responsive
# TODO columns should be enough...