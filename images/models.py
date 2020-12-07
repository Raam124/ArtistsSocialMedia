from django.db import models
from django.core.validators import URLValidator
from taggit.managers import TaggableManager
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.conf import settings
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils.crypto import get_random_string



def upload_location(instance, filename):
	file_path = 'image/{author_username}/{title}-{filename}'.format(
				author_username=str(instance.author.username),title=str(instance.title), filename=filename)
	return file_path


class Pictures(models.Model):
    title = models.CharField(max_length=200, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_location, null=True)
    tags = TaggableManager()
    description = models.TextField(max_length=10000, null=True, blank=True)
    slug = models.SlugField(
        max_length=250, unique_for_date='date_published', blank=True)
    category = models.CharField(max_length=50)
    date_published = models.DateField(
        auto_now_add=True, verbose_name="date published")
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='images_liked',blank=True)


    def __str__(self):
        return f"{self.title}-{self.date_published}"


class ContactUs(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    message = models.TextField(max_length=1000)

    def __str__(self):
        return f"{self.email}"


class Reports(models.Model):
    picture = models.ForeignKey(Pictures, verbose_name=(
        "Reports"), on_delete=models.CASCADE)
    reason = models.TextField(max_length=1000)

    def __str__(self):
        return f"{self.picture}"


@receiver(post_delete, sender=Pictures)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False) 




def pre_save_picture_receiver(sender, instance, *args, **kwargs):
    unique_slug_string = get_random_string(length=10)

    if not instance.slug:
        instance.slug = slugify(
            instance.title + "-" + instance.category + "-" + instance.author.username + "-" + unique_slug_string )


pre_save.connect(pre_save_picture_receiver, sender=Pictures)
