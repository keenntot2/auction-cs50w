from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models import Max
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import *
from .utils import secure_username


def index(request):
    if request.user.is_authenticated:
        watchlistCount = Watchlist.objects.get(user = User.objects.get(pk=request.user.id)).listing.count()
    else:
        watchlistCount = None
    return render(request, "auctions/index.html", {
        'listings' : Listing.objects.all().order_by('-id'),
        'watchlistCount' : watchlistCount
    })

def login_view(request):
    if  request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))
    else:
        if request.method == "POST":

            # Attempt to sign user in
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)

            # Check if authentication successful
            if user is not None:
                login(request, user)
                if not request.GET.get('next'):
                    return HttpResponseRedirect(reverse('index'))
                return HttpResponseRedirect(request.GET.get('next', '/'))
            else:
                return render(request, "auctions/login.html", {
                    "message": "Invalid username and/or password."
                })
        else:
            return render(request, "auctions/login.html")

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


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
        Watchlist(user=User.objects.get(pk=request.user.id)).save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
    
@login_required
def new(request):
    category = Category.objects.all()
    if request.method == "POST":
        form = CreateListing(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            startingBid = float(form.cleaned_data['startingBid'])
            image = form.cleaned_data['image']
            category = form.cleaned_data['category']
            seller_id = User.objects.get(pk=(request.user.id))
            if not image:
                Listing(seller = seller_id, title=title, description=description, startingBid=startingBid, category=Category.objects.get(pk=category)).save()
            else:
                Listing(seller = seller_id, title=title, description=description, startingBid=startingBid, image=image, category=Category.objects.get(pk=category)).save()
            return HttpResponseRedirect(reverse('index'))
            # return HttpResponse(f"{title} {description} ${'{:.2f}'.format(startingBid)} {image} {Category.objects.get(pk = category)}")
    return render(request, 'auctions/new.html', {
        'form' : CreateListing(),
        'watchlistCount' : Watchlist.objects.get(user = User.objects.get(pk=request.user.id)).listing.count()
    })

@login_required
def listing(request, listing_name, listing_id):
    item = Listing.objects.filter(pk=listing_id).first()
    watchlist = Watchlist.objects.get(user = User.objects.get(pk=request.user.id)).listing.filter(id=listing_id).first()
    error = []
    if request.method == 'POST':
        submitBtn = request.POST['submitBtn'].lower()
        listing = Listing.objects.get(pk=listing_id)
        form = Feedback(request.POST)
        bidForm = BidForm(request.POST)
        
            
        if submitBtn == 'close listing':
            listing.availability = False
            listing.save()
            return HttpResponseRedirect(reverse('listing', args=[listing_name, listing_id]))
        elif submitBtn in ['add to watchlist', 'remove from watchlist']:
            if watchlist:
                # watchlist.delete()
                Watchlist.objects.get(user = User.objects.get(pk=request.user.id)).listing.remove(listing)
                pass
            else:
                Watchlist.objects.get(user = User.objects.get(pk=request.user.id)).listing.add(listing)
            return HttpResponseRedirect(reverse('listing', args=[listing_name, listing_id]))
        elif form.is_valid() and submitBtn == 'add comment':
            feedback = form.cleaned_data['feedback']
            Comment(user = User.objects.get(pk=request.user.id),
                    listing = Listing.objects.get(pk=listing_id),
                    comment = feedback).save()
            return HttpResponseRedirect(reverse('listing', args=[listing_name, listing_id]))
        elif bidForm.is_valid() and submitBtn == 'bid':
            bid = bidForm.cleaned_data['bid']
            startingPrice = Listing.objects.get(pk=listing_id).startingBid
            highestBid = listing.bidItem.aggregate(highest_bid=Max('bid'))['highest_bid']
            if not highestBid:
                if bid >= startingPrice:
                    Bid(bidder=User.objects.get(pk=request.user.id),
                        listing = listing,
                        bid = bid).save()
                else:
                    error.append("Ensure that your bid is at least equal to the initial bidding amount.")
            elif bid < startingPrice:
                error.append("Ensure that your bid is at least equal to the initial bidding amount.")
            else:
                if bid>highestBid:
                    Bid(bidder=User.objects.get(pk=request.user.id),
                        listing = listing,
                        bid = bid).save()
                else: 
                    error.append("Another bidder has placed a higher bid than yours.")
        else:
            error.append("Invalid action.")
    return render(request, 'auctions/listing.html', {
        'item' : item,
        'listing_name' : listing_name,
        'watchlist' : watchlist,
        'watchlistCount' : Watchlist.objects.get(user = User.objects.get(pk=request.user.id)).listing.count(),
        'commentForm' : Feedback(),
        'bidForm' : BidForm(),
        'feedback' : [{'user_priv':secure_username(i.user.username), 'comment' : i.comment} for i in item.listingComment.all()],        
        'error' : error
    })

@login_required
def watchlist(request):
    watchlist = Watchlist.objects.get(user = User.objects.get(pk=1)).listing.all().order_by('-id')
    return render(request, 'auctions/watchlist.html', {
        'watchlist' : watchlist,
        'watchlistCount' : Watchlist.objects.get(user = User.objects.get(pk=request.user.id)).listing.count()
    })

@login_required
def categories(request):
    return render(request, 'auctions/categories.html', {
        'categories' : Category.objects.all(),
        'watchlistCount' : Watchlist.objects.get(user = User.objects.get(pk=request.user.id)).listing.count()
    })

@login_required
def category(request, category_id):
    return render(request, 'auctions/category.html', {
        "category" : Category.objects.get(pk=category_id),
        "listings" : Category.objects.get(pk=category_id).listingCategory.all(),
        'watchlistCount' : Watchlist.objects.get(user = User.objects.get(pk=request.user.id)).listing.count()
    })

@login_required
def bids(request):
    bids = Bid.objects.filter(bidder=User.objects.get(pk=request.user.id)).order_by('-id')
    listing = [{'listing' : item.listing,
                'nBid' : item.listing.bidItem.count(),
                'highestBidder' : Bid.objects.filter(bid = item.listing.bidItem.aggregate(highest_bid = Max('bid'))['highest_bid']).first().bidder.id,
                'highestBid' : item.listing.bidItem.aggregate(highest_bid = Max('bid'))['highest_bid'] } for item in bids]
    return render(request, 'auctions/bids.html', {
        'listings' : listing,
        'watchlistCount' : Watchlist.objects.get(user = User.objects.get(pk=request.user.id)).listing.count()
    })

@login_required
def selling(request):
    return render(request, 'auctions/selling.html', {
        'listings' : Listing.objects.filter(seller=User.objects.get(pk=request.user.id)).order_by('-id'),
        'watchlistCount' : Watchlist.objects.get(user = User.objects.get(pk=request.user.id)).listing.count()
    })
    
