from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.aggregates import Max
from django.db.models.fields import IntegerField, related


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=64)
    # listings = models.ManyToManyField(Listing, blank=True, related_name="categories")

    def __str__(self):
        return f"{self.name}"

class Bid(models.Model):
    amount = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey('Listing', on_delete=models.CASCADE, related_name="bids")
    time = models.DateTimeField(auto_now_add=True)

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=512)
    # current_bid = models.ForeignKey(Bid, related_name="listing")
    starting_bid = models.IntegerField()
    image_url = models.URLField(blank=True)
    category = models.ManyToManyField(Category, blank=True, related_name="listings")

    def __str__(self):
        return f"{self.title} (current bid {self.current_bid}): {self.description}"

class ListingComment(models.Model):
    user = models.CharField(max_length=64)
    content = models.TextField()

