from django.db import models
from django.contrib.auth.models import User
import time
# Create your models here.

class Breweries(models.Model):

    name = models.CharField(max_length=100)
    img = models.CharField(max_length=250)
    bio = models.TextField(max_length=500)
    verified_breweries = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
# New auth code for one to many relation user and breweriess
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Beer(models.Model):

    title = models.CharField(max_length=150)
    length = models.IntegerField(default=0)
    breweries = models.ForeignKey(
        Breweries, on_delete=models.CASCADE, related_name="beers")

    def __str__(self):
        return self.title

    def get_length(self):
        return time.strftime("%-M:%S", time.gmtime(self.length))

class Favorite(models.Model):

    title = models.CharField(max_length=150)
    # this creates the many to many relationship AND join table between favorite and beers
    beers = models.ManyToManyField(Beer)
    
    def __str__(self):
        return self.title