from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("categories", views.categories, name="categories"),
    path("category-listings/<int:category_id>", views.category_listings, name="category-listings"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new-listing", views.new_listing, name="new-listing"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("watchlist-action", views.watchlist_action, name="watchlist-action"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("bid", views.bid, name="bid"),
    path("close-auction", views.close_auction, name="close-auction"),
    path("comment", views.comment, name="comment"),

    path("<str:msg>", views.index, name="index-message")
]
