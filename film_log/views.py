from datetime import timezone
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from .forms import CreateReviewForm, CreateProfileForm
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .models import Profile, Movie, Review, Watchlist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login

# Create your views here.
class ShowAllProfilesView(ListView):
    model = Profile
    template_name = 'film_log/show_all_profiles.html'
    context_object_name = 'profiles'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            try:
                # Get the current user's profile and pass it to the template
                user_profile = Profile.objects.get(user=self.request.user)
                context['user_profile_pk'] = user_profile.pk
            except Profile.DoesNotExist:
                context['user_profile_pk'] = None
        return context
    
class ProfileView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'film_log/profile.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        return get_object_or_404(Profile, user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        context['watchlist'] = profile.watchlist.all()
        context['reviews'] = Review.objects.filter(user=self.request.user)
        return context

class CreateProfileView(CreateView):
    form_class = CreateProfileForm
    template_name = 'film_log/create_profile_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'user_form' not in context:
            context['user_form'] = UserCreationForm()

        if self.request.user.is_authenticated:
            try:
                context['user_profile_pk'] = self.request.user.profile.pk
            except Profile.DoesNotExist:
                context['user_profile_pk'] = None

        return context

    def form_valid(self, form):
        user_form = UserCreationForm(self.request.POST)

        if user_form.is_valid():
            user = user_form.save()
            login(self.request, user)

            profile = form.save(commit=False)
            profile.user = user
            profile.save()

            self.object = profile

            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form, user_form=user_form))
    
    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.object.profile.pk})

class PostReviewView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = CreateReviewForm
    template_name = 'film_log/post_review.html'

    def form_valid(self, form):
        movie = form.cleaned_data['movie']
        if not movie:
            movie_title = form.cleaned_data['movie']
            movie_description = "No description provided."
            movie_release_date = timezone.now()
            movie_director = "Unknown"
            movie_genre = "Unknown"
            movie = Movie.objects.create(title=movie_title, description=movie_description,
                                         release_date=movie_release_date, director=movie_director,
                                         genre=movie_genre)

        review = form.save(commit=False)
        review.user = self.request.user
        review.save()

        return redirect('movie_detail', movie_id=movie.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            try:
                user_profile = Profile.objects.get(user=self.request.user)
                context['user_profile_pk'] = user_profile.pk
            except Profile.DoesNotExist:
                context['user_profile_pk'] = None
        return context

class CreateFriendView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        # Get the current user's profile
        profile = get_object_or_404(Profile, user=self.request.user)
        
        # Get the other profile that the user wants to add as a friend
        other = get_object_or_404(Profile, pk=kwargs['other_pk'])
        
        # Add the other profile as a friend
        profile.add_friend(other)
        
        # Redirect back to the user's profile
        return redirect('show_profile', pk=profile.pk)
    
class ShowFriendSuggestionsView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'film_log/friend_suggestions.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        return get_object_or_404(Profile, user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['friend_suggestions'] = self.object.get_friend_suggestions()
        return context

class MovieDetailView(DetailView):
    model = Movie
    template_name = 'film_log/movie_detail.html'
    context_object_name = 'movie'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        movie = self.get_object()
        reviews = Review.objects.filter(movie=movie)
        context['reviews'] = reviews
        return context

class WatchlistView(LoginRequiredMixin, ListView):
    model = Watchlist
    template_name = 'film_log/watchlist.html'
    context_object_name = 'watchlist'

    def get_queryset(self):
        # Show the watchlist for the logged-in user
        profile = get_object_or_404(Profile, user=self.request.user)
        return Watchlist.objects.filter(profile=profile)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(Profile, user=self.request.user)
        return context

class AddToWatchlistView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        profile = get_object_or_404(Profile, user=self.request.user)
        movie = get_object_or_404(Movie, pk=kwargs['movie_id'])

        # Add movie to the watchlist
        Watchlist.objects.get_or_create(profile=profile, movie=movie)

        return redirect('watchlist')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(Profile, user=self.request.user)
        return context