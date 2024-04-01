from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
import tempfile
import pytesseract
import re
import hashlib
import os
from datetime import datetime
from .models import CustomUser, Receipt, Store, Reward
# Create your views here.

def index(request):
    customer = request.user
    stores = Store.objects.all()
    receipts = Receipt.objects.filter(customer=request.user)

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
    
def extract_info(image_path):
    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
    text = pytesseract.image_to_string(image_path)

    stores = ["ZARA", "Nike", "Walmart"]
    price_patterns = [
        r'\s+TOTAL\s+(\d+\.\d+)',
        r'TOTAL\s+\d+\s+(\d+\.\d+)',
        r'TOTAL\s+(\d+\.\d+)'
    ]
    date_patterns = [
        r'(\d{2}/\d{2}/\d{2})',
        r'(\d{2}/\d{2}/\d{4})'
    ]

    total_price = "Unknown"
    extracted_date = "Unknown"
    store_name = "Unknown"

    # Extract the price
    for pattern in price_patterns:
        match = re.search(pattern, text)
        if match:
            total_price = match.group(1)
            break

    # Extract the store name
    for store in stores:
        pattern = re.compile(r'\b{}\b'.format(re.escape(store)), re.IGNORECASE)
        if re.search(pattern, text):
            store_name = store
            break

    for date in date_patterns:
        match = re.search(date, text)
        if match:
            extracted_date = match.group(1)

    return store_name, extracted_date, total_price

def generate_image_identifier(image_content):
    image_hash = hashlib.sha256(image_content).hexdigest()
    return image_hash

def scan_receipts(request):
    if request.method == 'POST':
        image_file = request.FILES.get('receipt_image')
        if image_file:
            image_content = image_file.read()
            image_identifier = generate_image_identifier(image_content)
            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_image:
                temp_image.write(image_content)
                temp_image_path = temp_image.name
            store_name, date, total_price = extract_info(temp_image_path)

            try_formats = ['%d/%m/%Y', '%m/%d/%Y', '%m/%d/%y', '%d/%m/%y']
            parsed_date = None
            for format in try_formats:
                try:
                    parsed_date = datetime.strptime(date, format)
                    break
                except ValueError:
                    continue
            
            if parsed_date:
                date = parsed_date.strftime('%Y-%m-%d')
            else:
                date = None
            
            if Receipt.objects.filter(image_identifier=image_identifier).exists():
                print(image_identifier)
                return render(request, "points/scan_receipts.html", {
                    "message": "This receipt has already been scanned."
                })
            
            
            try:
                store_instance = Store.objects.get(name=store_name)
            except Store.DoesNotExist:
                return render(request, "points/scan_receipts.html", {
                "message": "Receipt could not be scanned."
            })

            current_user = request.user

            receipt = Receipt(raw_image=image_file, store=store_instance, date=date, amount=total_price, customer=current_user, image_identifier=image_identifier)
            receipt.save()

            total_price_int = int(float(total_price))
            current_user.active_points += total_price_int
            current_user.points_history += total_price_int
            current_user.save()
                
            return redirect('index')
            
    
    return render(request, "points/scan_receipts.html")

def reward_list(request):
    customer = request.user
    rewards = Reward.objects.all()
    return render(request, "points/reward_list.html", {
        "user" : customer,
        "rewards": rewards
    })

def create_reward(request):
    if request.method == "POST":

        name = request.POST["reward_name"]
        points = request.POST["points_requirement"]



        new_reward = Reward(
            reward_name= name,
            points_requirement= points,
            )
        new_reward.save()

        return HttpResponseRedirect(reverse("reward_list"))
    else:
        return render(request, "points/create_reward.html")
    
def redeem_reward(request, reward_id):
    user = request.user
    reward = Reward.objects.get(pk=reward_id)

    if reward.points_requirement <= user.active_points and reward not in user.rewards.all():
        user.active_points -= reward.points_requirement
        user.rewards.add(reward)
        user.save()  
    else:
        messages.error(request, "You don't have enough points to redeem this reward.")
    
    return HttpResponseRedirect(reverse("reward_list"))