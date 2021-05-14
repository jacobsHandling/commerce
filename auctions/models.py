from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields import IntegerField, related


class User(AbstractUser):
    pass


class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=512)
    current_bid = models.IntegerField()
    image_url = models.URLField(blank=True)

    def __str__(self):
        return f"{self.title} (current bid {self.current_bid}): {self.description}"

class Bid(models.Model):
    amount = models.IntegerField()

class ListingComment(models.Model):
    user = models.CharField(max_length=64)
    content = models.TextField()

class Category(models.Model):
    name = models.CharField(max_length=64)
    listings = models.ManyToManyField(Listing, blank=True, related_name="categories")

    def __str__(self):
        return f"{self.name}"