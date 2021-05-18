from typing import List
from auctions.models import User, Listing, Bid, ListingComment#, Category
from django.contrib import admin

# Register your models here.
admin.site.register(User)
admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(ListingComment)
# admin.site.register(Category)