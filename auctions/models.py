from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone



class User(AbstractUser):
    pass

class Category(models.Model):
    category = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.category}"
    
class Listing(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ownListings")
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=5000)
    startingBid = models.DecimalField(decimal_places=2,
                                      max_digits=10)
    image = models.CharField(max_length=5000,
                             default="https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Question_mark_%28black%29.svg/800px-Question_mark_%28black%29.svg.png")
    timestamp = models.DateTimeField(default=timezone.now, editable=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='listingCategory')
    availability = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.title} at a starting bid of ${'{:.2f}'.format(self.startingBid)}"

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userWatchlist')
    # listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listingWatchlist")
    listing = models.ManyToManyField(Listing, blank=True)

    # def __str__(self):
    #     return f"{self.listing}"
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenter")
    comment = models.CharField(max_length=200)
    # listing = models.ManyToManyField(Listing, blank=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listingComment", null=True)
    

    def __str__(self):
        return f"{self.user.username} commented '{self.comment}' on {self.listing.title}"
    
class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="buyer")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bidItem")
    bid = models.DecimalField(decimal_places=2,max_digits=10)

    def __str__(self):
        return f"{self.bidder.username} bids ${'{:.2f}'.format(self.bid)} on the {self.listing.title}"