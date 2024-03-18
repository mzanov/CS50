from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import *
# Create your views here.

def index(request):
    customer = request.user
    stores = Store.objects.all()
    receipts = Receipts.objects.filter(customer=request.user)

    return render(request, "points/index.html", {
        "user" : customer,
        "stores": stores,
        "receipts": receipts
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
            return render(request, "points/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "points/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        birthday = request.POST["birthday"]
        picture = request.POST["picture"]
        phone = request.POST["phone"]
        
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "points/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = CustomUser.objects.create_user(username=username, email=email, password=password)
            user.first_name = first_name
            user.last_name = last_name
            user.birthday = birthday
            user.picture = picture
            user.phone = phone
            user.save()
        except IntegrityError:
            return render(request, "points/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "points/register.html")
    
def add_store(request):
    if request.method == "POST":

        name = request.POST["name"]
        address = request.POST["address"]



        new_store = Store(
            name= name,
            address= address,
            )
        new_store.save()

        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "points/add_store.html")
    
def scan_receipts(request):
    if request.method == 'POST':
        user = request.user
        raw_image = request.POST['raw_image']
        amount = request.POST['amount']
        date = request.POST['date'] 
        store_name = request.POST['store']
        address = request.POST['address']


        store = Store.objects.filter(name=store_name).first()

        # Create a new Receipt object with the received data
        receipt = Receipts.objects.create(
            raw_image=raw_image,
            amount=amount,
            date=date,
            store=store,
            address=address,
            customer=user  # Assuming you have a logged-in user associated with the receipt
        )

        
        return redirect('index')  # Replace 'success_page' with the name of your success page URL pattern

    return render(request, 'points/scan_receipts.html')