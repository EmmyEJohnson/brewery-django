from django.contrib import admin
from .models import Breweries, Beer, Favorite
# Register your models here.
admin.site.register(Breweries)
admin.site.register(Beer)
admin.site.register(Favorite)


