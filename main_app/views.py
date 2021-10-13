from django.shortcuts import render, redirect, reverse
from django.views import View  # <- View class to handle requests
# <- a class to handle sending a type of response
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView
from .models import Breweries, Beer, Favorite

# at top of file with other imports
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
# Auth
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


# Main Views
class Home(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["favorites"] = Favorite.objects.all()
        return context

class About(TemplateView):
    template_name = "about.html"

class Signup(View):
    # show a form to fill out
    def get(self, request):
        form = UserCreationForm()
        context = {"form": form}
        return render(request, "registration/signup.html", context)
    # on form submit validate the form and login the user.
    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("breweries_list")
        else:
            context = {"form": form}
            return render(request, "registration/signup.html", context)


# Breweries Views
class BreweriesCreate(CreateView):
    model = Breweries
    fields = ['name', 'img', 'bio', 'verified_breweries']
    template_name = "breweries_create.html"
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(BreweriesCreate, self).form_valid(form)
    
    def get_success_url(self):
        print(self.kwargs)
        return reverse('breweries_detail', kwargs={'pk': self.object.pk})
    
    success_url = "/breweries/"


class BreweriesUpdate(UpdateView):
    model = Breweries
    fields = ['name', 'img', 'bio', 'verified_breweries']
    template_name = "breweries_update.html"
    success_url = "/breweries/"


@method_decorator(login_required, name='dispatch')
class BreweriesDetail(DetailView):
    model = Breweries
    template_name = "breweries_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["favorites"] = Favorite.objects.all()
        return context


class BreweriesDelete(DeleteView):
    model = Breweries
    template_name = "breweries_delete_confirmation.html"
    success_url = "/breweries/"

@method_decorator(login_required, name='dispatch')
class BreweriesList(TemplateView):
    template_name = "breweries_list.html"

    def get_context_data(self, **kwargs):
        print(Breweries)
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name")
        if name != None:
            # .filter is the sql WHERE statement and name__icontains is doing a search for any name that contains the query param
            context["breweries"] = Breweries.objects.filter(name__icontains=name, user=self.request.user)
            context["header"] = f"Searching for \"{name}\""
        else:
            context["breweries"] = Breweries.objects.filter(user=self.request.user)
            context["header"] = "Trending Breweries"
        return context

class BeerCreate(View):

    def post(self, request, pk):
        title = request.POST.get("title")
        length = request.POST.get("length")
        breweries = Breweries.objects.get(pk=pk)
        Beer.objects.create(title=title, length=length, breweries=breweries)
        return redirect('breweries_detail', pk=pk)

class BeerList(TemplateView):
    template_name = 'beer_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # this is where we add the key into our context object for the view to use
        context["beers"] = []
        return context

class FavoriteBeerAssoc(View):

    def get(self, request, pk, beer_pk):
        # get query param from URL
        assoc = request.GET.get("assoc")
        if assoc == "remove":
            # get the favorite by the id and
            # remove from the join table the given beer_id
            Favorite.objects.get(pk=pk).beers.remove(beer_pk)
        if assoc == "add":
            # get the favorite by the id and
            # add to the join table the given beer_id
            Favorite.objects.get(pk=pk).beers.add(beer_pk)
        return redirect('home')