from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.aggregates import Max
from django.db.models.fields import IntegerField, related


class User(AbstractUser):
    watchlist = models.ManyToManyField('Listing', blank=True, related_name="watchers")

    def __str__(self):
        return f"{self.username}"
# class Category(models.Model):
#     name = models.CharField(max_length=64)
#     # listings = models.ManyToManyField(Listing, blank=True, related_name="categories")

#     def __str__(self):
#         return f"{self.name}"

class Bid(models.Model):
    amount = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey('Listing', on_delete=models.CASCADE, related_name="bids")
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-time',)

    def __str__(self):
        return f"{self.amount} / {self.user} / {self.time}"

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=512)
    # current_bid = models.ForeignKey(Bid, related_name="listing")
    current_price = models.IntegerField()
    starting_price = models.IntegerField()
    image_url = models.URLField(blank=True, max_length=512)
    # category = models.ManyToManyField(Category, blank=True, related_name="listings")
    category = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return f"{self.title}: {self.description}\n"

class ListingComment(models.Model):
    user = models.CharField(max_length=64)
    content = models.TextField()

