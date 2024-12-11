from datetime import timezone
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from .forms import CreateReviewForm, CreateProfileForm, CreateMovieForm, UpdateProfileForm, UpdateReviewForm
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .models import UserProfile, Movie, Review, Watchlist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.db.models import Avg

# Create your views here.
class ShowAllView(ListView):
    model = UserProfile
    template_name = 'film_log/show_all.html'
    context_object_name = 'profiles'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            try:
                user_profile = UserProfile.objects.get(user=self.request.user)
                context['user_profile_pk'] = user_profile.pk
            except UserProfile.DoesNotExist:
                context['user_profile_pk'] = None
        return context
    
class ProfileView(DetailView):
    model = UserProfile
    template_name = 'film_log/profile.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        profile_pk = self.kwargs.get("pk")
        if not profile_pk:
            # Fallback to the logged-in user's profile if no pk is provided
            return get_object_or_404(UserProfile, user=self.request.user)
        return get_object_or_404(UserProfile, pk=profile_pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()

        if self.request.user.is_authenticated:
            try:
                user_profile = UserProfile.objects.get(user=self.request.user)
                context['user_profile_pk'] = user_profile.pk
            except UserProfile.DoesNotExist:
                context['user_profile_pk'] = None

        # Query reviews for the profile using 'userProfile'
        context['reviews'] = Review.objects.filter(userProfile=profile).order_by('-date_posted')
        context['watchlist'] = profile.watchlist.all()
        return context

class MovieListView(ListView):
    model = Movie
    template_name = 'film_log/all_movies.html'
    context_object_name = 'movies'

    def get_queryset(self):
        query = self.request.GET.get('q', '')  # Get the search term from the request
        if query:
            return Movie.objects.filter(title__icontains=query)  # Filter movies by title
        return Movie.objects.all()  # Show all movies if no search term

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        query = self.request.GET.get('q', '')
        context['query'] = query

        if self.request.user.is_authenticated:
            try:
                user_profile = UserProfile.objects.get(user=self.request.user)
                context['user_profile_pk'] = user_profile.pk
            except UserProfile.DoesNotExist:
                context['user_profile_pk'] = None
        return context

class CreateProfileView(CreateView):
    form_class = CreateProfileForm
    template_name = 'film_log/create_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_form'] = UserCreationForm()
        if self.request.user.is_authenticated:
            try:
                user_profile = UserProfile.objects.get(user=self.request.user)
                context['user_profile_pk'] = user_profile.pk
            except UserProfile.DoesNotExist:
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
        return reverse('profile', kwargs={'pk': self.object.pk})

class PostReviewView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = CreateReviewForm
    template_name = 'film_log/post_review.html'

    def form_valid(self, form):
        # Get the user's profile
        user_profile = self.request.user.profile  # Access via related_name in UserProfile

        # Check if the movie exists, create one if it doesn't
        movie = form.cleaned_data.get('movie')
        if not movie:
            movie_title = form.cleaned_data['movie']
            movie_description = "No description provided."
            movie_release_date = timezone.now()
            movie_director = "Unknown"
            movie_genre = "Unknown"
            movie = Movie.objects.create(
                title=movie_title, 
                description=movie_description,
                release_date=movie_release_date, 
                director=movie_director,
                genre=movie_genre
            )

        # Save the review and link it to the user's profile
        review = form.save(commit=False)
        review.userProfile = user_profile  # Associate with UserProfile, not User
        review.save()

        return redirect('show_movie', pk=movie.pk)  # Adjust redirect to use `pk`

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            try:
                user_profile = UserProfile.objects.get(user=self.request.user)
                context['user_profile_pk'] = user_profile.pk
            except UserProfile.DoesNotExist:
                context['user_profile_pk'] = None

        # Provide list of movies to search for
        context['movies'] = Movie.objects.all()
        return context

    
class CreateFriendView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        # Get the current user's profile
        profile = get_object_or_404(UserProfile, user=self.request.user)
        
        # Get the other profile that the user wants to add as a friend
        other = get_object_or_404(UserProfile, pk=kwargs['other_pk'])
        
        # Add the other profile as a friend
        profile.add_friend(other)
        
        # Redirect back to the user's profile
        return redirect('profile', pk=profile.pk)
    
class ShowFriendSuggestionsView(LoginRequiredMixin, DetailView):
    model = UserProfile
    template_name = 'film_log/friend_suggestions.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        return get_object_or_404(UserProfile, user=self.request.user)

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
        if self.request.user.is_authenticated:
            try:
                user_profile = UserProfile.objects.get(user=self.request.user)
                context['user_profile_pk'] = user_profile.pk
            except UserProfile.DoesNotExist:
                context['user_profile_pk'] = None
        movie = self.get_object()
        reviews = Review.objects.filter(movie=movie)
        average_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
        context.update({
            'reviews': reviews,
            'average_rating': average_rating,
        })
        return context

class WatchlistView(LoginRequiredMixin, ListView):
    model = Watchlist
    template_name = 'film_log/watchlist.html'
    context_object_name = 'watchlist'

    def get_queryset(self):
        # Get the watchlist for the logged-in user
        profile = get_object_or_404(UserProfile, user=self.request.user)
        return Watchlist.objects.filter(userProfile=profile).select_related('movie')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        watchlist_items = self.get_queryset()

        if self.request.user.is_authenticated:
            try:
                user_profile = UserProfile.objects.get(user=self.request.user)
                context['user_profile_pk'] = user_profile.pk
            except UserProfile.DoesNotExist:
                context['user_profile_pk'] = None

        # Build a list of movie details for the template
        context['movies'] = [
            {
                "id": item.movie.id,
                "title": item.movie.title,
                "release_date": item.movie.release_date,
                "description": item.movie.description,
                "director": item.movie.director,
                "genre": item.movie.genre,
                "poster": item.movie.poster.url if item.movie.poster else None,
            }
            for item in watchlist_items
        ]
        return context


class AddToWatchlistView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        profile = get_object_or_404(UserProfile, user=self.request.user)
        movie = get_object_or_404(Movie, pk=kwargs['movie_id'])

        # Add movie to the watchlist
        Watchlist.objects.get_or_create(profile=profile, movie=movie)

        return redirect('watchlist')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(UserProfile, user=self.request.user)
        return context

class RemoveFromWatchlistView(LoginRequiredMixin, View):
    def post(self, request, pk):
        # Get the logged-in user's profile
        user_profile = get_object_or_404(UserProfile, user=request.user)
        
        # Get the specific movie
        movie = get_object_or_404(Movie, pk=pk)
        
        # Delete the watchlist entry for this movie and user profile
        watchlist_entry = get_object_or_404(Watchlist, userProfile=user_profile, movie=movie)
        watchlist_entry.delete()

        # Redirect back to the watchlist
        return redirect('watchlist')


class CreateMovieView(LoginRequiredMixin, CreateView):
    model = Movie
    form_class = CreateMovieForm
    template_name = 'film_log/add_movie.html'
    context_object_name = 'movie'

    def form_valid(self, form):
        # Handle the form submission to create a new movie
        movie = form.save(commit=False)
        movie.save()
        return redirect('show_movie', pk=movie.pk)  # Redirect to the newly created movie's detail page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            try:
                user_profile = UserProfile.objects.get(user=self.request.user)
                context['user_profile_pk'] = user_profile.pk
            except UserProfile.DoesNotExist:
                context['user_profile_pk'] = None
        return context

class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = UpdateProfileForm
    template_name = 'film_log/update_profile.html'

    def get_object(self, queryset=None):
        # Ensure the user can only update their own profile
        return get_object_or_404(UserProfile, user=self.request.user)

    def get_success_url(self):
        # Redirect to the profile page after successful update
        return reverse('profile', kwargs={'pk': self.object.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            try:
                user_profile = UserProfile.objects.get(user=self.request.user)
                context['user_profile_pk'] = user_profile.pk
            except UserProfile.DoesNotExist:
                context['user_profile_pk'] = None
        return context
    
class UpdateReviewView(LoginRequiredMixin, UpdateView):
    model = Review
    form_class = UpdateReviewForm
    template_name = 'film_log/update_review.html'

    def get_object(self, queryset=None):
        # Ensure only the author can update the review
        review = get_object_or_404(Review, pk=self.kwargs['pk'])
        return review

    def get_success_url(self):
        # Redirect to the movie's detail page after a successful update
        return reverse('show_movie', kwargs={'pk': self.object.movie.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            try:
                user_profile = UserProfile.objects.get(user=self.request.user)
                context['user_profile_pk'] = user_profile.pk
            except UserProfile.DoesNotExist:
                context['user_profile_pk'] = None
        return context