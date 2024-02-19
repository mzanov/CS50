from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import *

def index(request):
    active_listings = Listing.objects.filter(is_active=True).order_by('-title')
    categories = Category.objects.all()
    return render(request, "auctions/index.html", {
    "active_listings": active_listings,
    "categories": categories
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

def create_listing(request):
    if request.method == "POST":

        title = request.POST["title"]
        description = request.POST["description"]
        image = request.POST["image"]
        price = request.POST["price"]
        category_name = request.POST["category"]

        if not Category.objects.filter(name=category_name).exists():
            category = Category.objects.create(name=category_name)
        else:
            category = Category.objects.get(name=category_name)

        bid = Bid(
            bidder=request.user,
            bid=float(price),
            )
        bid.save()


        new_listing = Listing(
            title=title,
            description=description,
            image=image,
            price=bid,
            category= category,
            owner=request.user
            )
        new_listing.save()

        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/create_listing.html")


def display_category(request):
    if request.method == "POST":
        listings = Listing.objects.filter(is_active=True, category=Category.objects.get(name=request.POST["category"]))

        categories = Category.objects.all()

        return render(request, "auctions/index.html", {
            "active_listings": listings,
            "categories": categories
        })



def listing_details(request, listing_id):

    is_active = Listing.objects.get(pk=listing_id).is_active

    if is_active == False:
            return render(request, "auctions/index.html", {
            "message": "The listing is closed"
        })
    
    else:
        return render(request, "auctions/listing_details.html", {
        "listing": Listing.objects.get(pk=listing_id),
        "watchlist": Listing.objects.get(pk=listing_id).watchlist.filter(username=request.user.username).exists(),
        "comments": Comment.objects.filter(listing=listing_id),
        "error_message": "No error.",
        "is_owner": Listing.objects.get(pk=listing_id).owner.username == request.user.username,
        "is_active": is_active,
    })




def get_watchlist_page(request):

    if not request.user.is_authenticated:
        return render(request, "auctions/login.html", {
            "message": "Please login to view your watchlist."
        })


    user = request.user
    listings = user.watchlist.all()

    return render(request, "auctions/watchlist.html", {
        "listings": listings
        })


def add_watchlist(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    listing.watchlist.add(request.user)

    return HttpResponseRedirect(reverse("listing_details", args=(listing_id,)))

def place_bid(request, listing_id):
    if request.method == 'POST':

        listing = Listing.objects.get(pk=listing_id)

        bid_amount =  (float) (request.POST.get('bid'))

        current_bid = Listing.objects.get(pk=listing_id).price.bid

        if bid_amount > current_bid:
            new_bid = Bid(
            bidder=request.user,
            bid=bid_amount
            )
            new_bid.save()

            listing = Listing.objects.get(pk=listing_id)
            listing.price = new_bid
            listing.save()
            return redirect('listing_details', listing_id=listing_id)
        
    return HttpResponseRedirect(reverse('listing_details', args=(listing_id,)))

def close_listing(request, listing_id):

    listing = Listing.objects.get(pk=listing_id)

    listing.is_active = False
    listing.save()

    return render(request, "auctions/listing_details.html", {
            "listing": Listing.objects.get(pk=listing_id),
            "watchlist": Listing.objects.get(pk=listing_id).watchlist.filter(username=request.user.username).exists(),
            "comments": Comment.objects.filter(listing=listing_id),
            "message": "Listing closed.",
            "update": True,
            "error": False,
            "is_active": False,
        })


def remove_watchlist(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    listing.watchlist.remove(request.user)

    return HttpResponseRedirect(reverse("listing_details", args=(listing_id,)))

def add_comment(request, listing_id):
    # Create new comment
    new_comment = Comment(
        author=request.user,
        listing=Listing.objects.get(pk=listing_id),
        comment=request.POST["comment"]
        )
    new_comment.save()

    return HttpResponseRedirect(reverse("listing_details", args=(listing_id,)))