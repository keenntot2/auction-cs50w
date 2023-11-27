from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin
from .models import *


# Register your models here.
class ListingAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'seller',
                    'title',
                    'availability',
                    'description',
                    'startingBid',
                    'category',
                    'timestamp')

class WatchlistAdmin(admin.ModelAdmin):
    list_display = ('user',
                    'listing')
    
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user',
                    'comment',
                    'listing')
    
class BidAdmin(admin.ModelAdmin):
    list_display= ('bidder',
                   'bid',
                   'listing')

admin.site.register(User, UserAdmin)
admin.site.register(Category)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Watchlist, WatchlistAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Bid, BidAdmin)
