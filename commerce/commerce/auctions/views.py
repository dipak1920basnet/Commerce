from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, Category, Auction_listing, Comment, Bid
from django.contrib import messages

def index(request):
    return render(request, "auctions/index.html",
                      {
                          "active_list":Auction_listing.objects.all(),
                          "Category":Category.objects.all(),
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





## Creating a listing
@login_required
def create(request):
    return render(request, "auctions/create.html", {
        "Category":Category.objects.all(),
    })

## Get created listing data
@login_required
def create_listing(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        url = request.POST.get("url")
        category = request.POST.get("Category")
        starting_bid = int(request.POST.get("min_bid"))

        # Create category and save category if category not in category
        category_instance = Category.objects.get(category_field=category)
        owner_instance = User.objects.get(username=request.user)
        #
        # if not category_instance:
            # Category.objects.create(category_field = category)
        # category_instance = Category.objects.filter(category_field = category).first()
        #Get the name of user 
        # user = User().objects.all()
        listing = Auction_listing.objects.create(title = title, description = description,starting_bid = starting_bid, image_url=url, category=category_instance, owner=owner_instance)
        # if listing.is_valid():
        listing.save()
        
        return HttpResponseRedirect(reverse('index'))
    

    
## View list of categories 
def categories(request):
    return render(request, "auctions/categories.html",
                  {
                      "Category_List": Category.objects.all()
                  })

## View item from categories:
def view_item_categories(request, category_name):
    category = Category.objects.get(category_field = category_name)
    return render(request, "auctions/category_item.html",
                  {
                      "category_name":category_name,
                      "category_name_list": category.category.all()
                  })
