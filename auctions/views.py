from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Bid, ListingComment
from .forms import ListingForm



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

    listing = Listing.objects.get(id=listing_id)
    bids = Bid.objects.filter(listing_id=listing_id)
    watching = bool(listing.watchers.filter(id=request.user.id))  # this can be cleaner?
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "bids": bids,
        "watching": watching
    })

def watch(request):
    if request.method == "POST":
        listing_id = int(request.POST["listing_id"])
        listing = Listing.objects.get(pk=listing_id)
        request.user.watchlist.add(listing)
        return HttpResponseRedirect(reverse("listing", args=[listing_id]))

def unwatch(request, listing_id):
    pass