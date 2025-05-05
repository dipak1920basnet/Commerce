from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    
    pass

# Your application should have at least three models in addition to the User model: 

# Models for Category
class Category(models.Model):
    
    category_field = models.CharField(max_length=200)
    def __str__(self):
        return f"{self.category_field}"

# one for auction listings
class Auction_listing(models.Model):
    
    # a title for the listing,
    title = models.CharField(max_length=30)
    #  a text-based description, 
    description = models.CharField(max_length=300) 
    # what the starting bid should be.
    starting_bid = models.IntegerField(blank=False)
    # Users should also optionally be able to provide a URL for an image
    image_url = models.URLField(null=True, blank=True)

    # and/or a category
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='user')
    is_active = models.BooleanField(default=True)
    # comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="comments")
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name='onwatchlist')

    def __str__(self):
        return f"{self.title} {self.description}"
    


# # one for comments made on auction listings.
class Comment(models.Model):
    # Get the comment
    
    auction_listing = models.ForeignKey(Auction_listing, on_delete=models.CASCADE, related_name="auction_llist")
    comment = models.CharField(max_length=200, blank=True, unique=False)

    def __str__(self):
        return f"{self.comment}"
    
## Models for bid
class Bid(models.Model):
    auction_listing = models.ForeignKey(Auction_listing, on_delete=models.CASCADE, related_name="list", null=True, blank=True)
    bidder_name = models.ForeignKey(User, related_name="bidder", on_delete=models.CASCADE, null=True, blank=True)
    bidding_amount = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.bidding_amount}"
