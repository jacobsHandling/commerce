from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Bid, ListingComment
from .forms import ListingForm, PartialBidForm



def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {
        "listings": listings
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
        form = ListingForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "auctions/index.html", {
                "message": "New listing saved successfully!"
            })
    else:
        return render(request, "auctions/new_listing.html", {
            "form": ListingForm()
        })

def listing(request, listing_id):
    """Renders the page for a listing"""

    def determine_watchlist_action():

        def is_watching():
            return bool(listing.watchers.filter(id=request.user.id))

        if is_watching():  # this can be cleaner?
            return 0  #  present option to unwatch
        return 1

    listing = Listing.objects.get(id=listing_id)
    bids = Bid.objects.filter(listing_id=listing_id)

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "bids": bids,
        "bid_form": PartialBidForm(),
        "watchlist_action": determine_watchlist_action()
    })

@login_required
def watchlist_action(request):
    """Either adds or removes the listing to/from the user's watchlist."""
    if request.method == "POST":
        listing_id = int(request.POST["listing_id"])
        listing = Listing.objects.get(pk=listing_id)
        if int(request.POST["watchlist_action"]) == 1:
            request.user.watchlist.add(listing)
        else:
            request.user.watchlist.remove(listing)
        return HttpResponseRedirect(reverse("listing", args=[listing_id]))

@login_required
def bid(request):
    if request.method == "POST":
        listing = Listing.objects.get(pk=int(request.POST['listing_id']))
        bid_amount = int(request.POST['amount'])
        if bid_amount < listing.current_price:
            #go back to listing page, with error message
            pass
        else:
            bid = Bid(amount=bid_amount, user=request.user, listing=listing)
            bid.save()
            listing.current_price = bid_amount
            listing.save()
            return HttpResponseRedirect(reverse("listing", args=[listing.id]))   # with message "bid successful"
