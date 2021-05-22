from typing import List
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Bid, ListingComment
from .forms import ListingForm, PartialBidForm, PartialCommentForm



def index(request, success_msg=None):
    active_listings = Listing.objects.filter(is_active=True)
    message = None
    if success_msg == 'success':
        message = "Successfully added a new listing"
    return render(request, "auctions/index.html", {
        "active_listings": active_listings,
        "message": message
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def new_listing(request):
    """Handles creating a new listing"""
    if request.method == 'POST':
        listing_starter = Listing(current_price=request.POST['starting_price'], owner=request.user)
        listing = ListingForm(request.POST, instance=listing_starter)
        if listing.is_valid():
            listing.save()
            return HttpResponseRedirect(reverse("index-success", args=['success']))
            render(request, "auctions/index.html", {
                "message": "New listing saved successfully!"
            })
    else:
        return render(request, "auctions/new_listing.html", {
            "form": ListingForm()
        })

def listing(request, listing_id):
    """Renders the page for a listing"""

    # def determine_watchlist_action():

        # def is_watching():
        #     return not bool(listing.watchers.filter(id=request.user.id))

        # if is_watching():  # this can be cleaner?
        #     return 0  #  present option to unwatch
        # return 1

    listing = Listing.objects.get(id=listing_id)
    # bids = Bid.objects.filter(listing_id=listing_id)

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "bids": listing.bids.all(),
        "bid_form": PartialBidForm(),
        "comments": listing.comments.all(),
        "comment_form": PartialCommentForm(),
        "watchlist_action": not bool(listing.watchers.filter(id=request.user.id))
    })

@login_required
def watchlist_action(request):
    """Either adds or removes the listing to/from the user's watchlist."""
    if request.method == "POST":
        listing = Listing.objects.get(pk=int(request.POST["listing_id"]))
        if request.POST["watchlist_action"] == 'True':
            request.user.watchlist.add(listing)
        else:
            request.user.watchlist.remove(listing)
        return HttpResponseRedirect(reverse("listing", args=[listing.id]))

@login_required
def watchlist(request):
    watchlist = Listing.objects.filter(watchers__pk=request.user.pk)  # see https://docs.djangoproject.com/en/3.2/topics/db/queries/#lookups-that-span-relationships
    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist
    })
@login_required
def bid(request):
    if request.method == "POST":
        listing = Listing.objects.get(pk=int(request.POST['listing_id']))
        bid_amount = int(request.POST['amount'])
        if bid_amount < listing.current_price:
            #go back to listing page, with error message
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "bids": listing.bids.all(),
                "bid_form": PartialBidForm(),
                "watchlist_action": not bool(listing.watchers.filter(id=request.user.id)),
                "message": "Bid amount must be greater than the current price"
            })
        else:
            bid = Bid(amount=bid_amount, user=request.user, listing=listing)
            bid.save()
            listing.current_price = bid_amount
            listing.save()
            return HttpResponseRedirect(reverse("listing", args=[listing.id]))   # with message "bid successful"

def close_auction(request):
    if request.method=="POST":
        listing = Listing.objects.get(pk=int(request.POST['listing_id']))
        listing.is_active = False
        listing.winner = listing.bids.first().user
        listing.save()
        return HttpResponseRedirect(reverse('listing', args=[listing.id]))

@login_required
def comment(request):
    if request.method == "POST":
        listing = Listing.objects.get(pk=int(request.POST['listing_id']))
        new_comment = ListingComment(user=request.user, listing=listing, content=request.POST['comment'])
        new_comment.save()
        return HttpResponseRedirect(reverse('listing', args=[listing.id]))