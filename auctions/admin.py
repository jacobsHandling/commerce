from typing import List
from .models import User, Category, Bid, Listing, ListingComment
from django.contrib import admin

# Register your models here.
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Bid)
admin.site.register(Listing)
admin.site.register(ListingComment)