from django.urls import path
from . import views

# this like app.use() in express
urlpatterns = [
    path('', views.Home.as_view(), name="home")  ,
    path('about/', views.About.as_view(), name="about"),

    # BREWERIES ROUTES     
     path('breweries/', views.BreweriesList.as_view(),name="breweries_list"),
     path('breweries/new/', views.BreweriesCreate.as_view(  ), name="breweries_create"),
     path('breweries/<int:pk>/', views.BreweriesDetail.as_view(), name="breweries_detail"),
     path('breweries/<int:pk>/update', views.BreweriesUpdate.as_view(), name="breweries_update"),
     path('breweries/<int:pk>/delete', views.BreweriesDelete.as_view(), name="breweries_delete"),
     path('breweries/<int:pk>/beers/new/', views.BeerCreate.as_view(), name="beer_create"),
     path('beers/', views.BeerList.as_view(), name="beer_list"),
     path('favorites/<int:pk>/beers/<int:beer_pk>/', views.FavoriteBeerAssoc.as_view(), name="favorite_beer_assoc"),
     # our new view
     path('accounts/signup/', views.Signup.as_view(), name="signup")
]