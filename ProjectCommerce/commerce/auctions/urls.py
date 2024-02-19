from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    
    path("createListing", views.create_listing, name="create_listing"),
    path("listing/<int:listing_id>", views.listing_details, name="listing_details"),
    path("watchlist/", views.get_watchlist_page, name="watchlist"),
    path("addWatchlist/<int:listing_id>", views.add_watchlist, name="add_watchlist"),
    path("removeWatchlist/<int:listing_id>", views.remove_watchlist, name="remove_watchlist"),
    path("displayCategory", views.display_category, name="display_category"),
    path("placeBid/<int:listing_id>", views.place_bid, name="place_bid"),
    path("closeListing/<int:listing_id>", views.close_listing, name="close_listing"),
    path("addComment/<int:listing_id>", views.add_comment, name="add_comment"),
]
