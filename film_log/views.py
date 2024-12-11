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
from django.contrib import messages
from django.http import Http404

# Create your views here.
# Show all user profiles
class ShowAllView(ListView):
    model = UserProfile  # The model to query
    template_name = 'film_log/show_all.html'  # Template to render
    context_object_name = 'profiles'  # Name of the context variable

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Check if the user is authenticated and try to get their profile
        if self.request.user.is_authenticated:
            try:
                user_profile = UserProfile.objects.get(user=self.request.user)
                context['user_profile_pk'] = user_profile.pk  # Add user profile ID to context
            except UserProfile.DoesNotExist:
                context['user_profile_pk'] = None  # In case the user doesn't have a profile
        return context


# View for displaying a specific user profile
class ProfileView(DetailView):
    model = UserProfile  # The model to query
    template_name = 'film_log/profile.html'  # Template to render
    context_object_name = 'profile'  # Name of the context variable for the profile

    def get_object(self, queryset=None):
        # Get the profile based on pk in URL or fallback to logged-in user's profile
        profile_pk = self.kwargs.get("pk")
        if not profile_pk:
            return get_object_or_404(UserProfile, user=self.request.user)
        return get_object_or_404(UserProfile, pk=profile_pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        
        # Same logic to get and add the logged-in user's profile
        if self.request.user.is_authenticated:
            try:
                user_profile = UserProfile.objects.get(user=self.request.user)
                context['user_profile_pk'] = user_profile.pk
            except UserProfile.DoesNotExist:
                context['user_profile_pk'] = None

        # Get reviews and watchlist for the profile
        context['reviews'] = Review.objects.filter(userProfile=profile).order_by('-date_posted')
        context['watchlist'] = profile.watchlist.all()
        return context


# View for listing movies with optional search functionality
class MovieListView(ListView):
    model = Movie  # The model to query
    template_name = 'film_log/all_movies.html'  # Template to render
    context_object_name = 'movies'  # Name of the context variable for movies

    def get_queryset(self):
        # Get the search term from the request query
        query = self.request.GET.get('q', '')
        if query:
            # Filter movies by title if a search term is provided
            return Movie.objects.filter(title__icontains=query)
        return Movie.objects.all()  # Return all movies if no search term is provided

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the query string to context to show on the template
        query = self.request.GET.get('q', '')
        context['query'] = query

        # Same logic to add the logged-in user's profile if authenticated
        if self.request.user.is_authenticated:
            try:
                user_profile = UserProfile.objects.get(user=self.request.user)
                context['user_profile_pk'] = user_profile.pk
            except UserProfile.DoesNotExist:
                context['user_profile_pk'] = None
        return context


# View for creating a new user profile
class CreateProfileView(CreateView):
    form_class = CreateProfileForm  # The form to create a profile
    template_name = 'film_log/create_profile.html'  # Template to render

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add a user creation form to the context
        context['user_form'] = UserCreationForm()
        if self.request.user.is_authenticated:
            try:
                user_profile = UserProfile.objects.get(user=self.request.user)
                context['user_profile_pk'] = user_profile.pk
            except UserProfile.DoesNotExist:
                context['user_profile_pk'] = None
        return context

    def form_valid(self, form):
        # Handle form validation and user profile creation
        user_form = UserCreationForm(self.request.POST)
        if user_form.is_valid():
            user = user_form.save()  # Create the user
            login(self.request, user)  # Log the user in
            profile = form.save(commit=False)
            profile.user = user  # Associate the profile with the user
            profile.save()
            self.object = profile
            return redirect(self.get_success_url())  # Redirect to the new profile page
        else:
            return self.render_to_response(self.get_context_data(form=form, user_form=user_form))

    def get_success_url(self):
        # Success URL after profile creation
        return reverse('profile', kwargs={'pk': self.object.pk})


# View for posting a review
class PostReviewView(LoginRequiredMixin, CreateView):
    model = Review  # The model to query
    form_class = CreateReviewForm  # The form to create a review
    template_name = 'film_log/post_review.html'  # Template to render

    def form_valid(self, form):
        user_profile = self.request.user.profile  # Access the user's profile
        movie = form.cleaned_data.get('movie')  # Get the movie for the review

        if not movie:
            # If no movie is provided, create a new movie entry
            movie_title = form.cleaned_data['movie']
            movie_description = "No description provided."
            movie_release_date = timezone.now()
            movie = Movie.objects.create(
                title=movie_title, 
                description=movie_description,
                release_date=movie_release_date,
            )

        # Save the review and link it to the user's profile
        review = form.save(commit=False)
        review.userProfile = user_profile
        review.save()
        return redirect('show_movie', pk=movie.pk)  # Redirect to the movie detail page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            try:
                user_profile = UserProfile.objects.get(user=self.request.user)
                context['user_profile_pk'] = user_profile.pk
            except UserProfile.DoesNotExist:
                context['user_profile_pk'] = None
        # Add list of movies to the context to allow review selection
        context['movies'] = Movie.objects.all()
        return context

class DeleteReviewView(LoginRequiredMixin, DeleteView):
    model = Review
    template_name = 'film_log/delete_review.html'  # This is the template for confirming the deletion

    def get_success_url(self):
        # Redirect to the user's profile after successful deletion of the review
        return reverse('profile', kwargs={'pk': self.object.userProfile.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            try:
                user_profile = UserProfile.objects.get(user=self.request.user)
                context['user_profile_pk'] = user_profile.pk
            except UserProfile.DoesNotExist:
                context['user_profile_pk'] = None
        return context

# View for creating a friend relationship between users
class CreateFriendView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        profile = get_object_or_404(UserProfile, user=self.request.user)  # Get the logged-in user's profile
        other = get_object_or_404(UserProfile, pk=kwargs['other_pk'])  # Get the other user's profile
        profile.add_friend(other)  # Add the other profile as a friend
        return redirect('profile', pk=profile.pk)  # Redirect to the user's profile page


# View for suggesting friends to the user based on common interests
class ShowFriendSuggestionsView(LoginRequiredMixin, DetailView):
    model = UserProfile
    template_name = 'film_log/friend_suggestions.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        # Get the profile of the logged-in user
        return get_object_or_404(UserProfile, user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            try:
                user_profile = UserProfile.objects.get(user=self.request.user)
                context['user_profile_pk'] = user_profile.pk
            except UserProfile.DoesNotExist:
                context['user_profile_pk'] = None
        # Get a list of friend suggestions based on user profile
        context['friend_suggestions'] = self.object.get_friend_suggestions()
        return context


# View for showing details of a movie, including reviews and average rating
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
            'reviews': reviews,  # Reviews for the movie
            'average_rating': average_rating,  # Average rating of the movie
        })
        return context


# View for listing the movies in the user's watchlist
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
        if self.request.user.is_authenticated:
            try:
                user_profile = UserProfile.objects.get(user=self.request.user)
                context['user_profile_pk'] = user_profile.pk
            except UserProfile.DoesNotExist:
                context['user_profile_pk'] = None
        # Build a list of movie details for the template
        watchlist_items = self.get_queryset()
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


# View for adding a movie to the user's watchlist
class AddToWatchlistView(LoginRequiredMixin, View):
    def post(self, request, pk):
        # Get the logged-in user's profile
        user_profile = get_object_or_404(UserProfile, user=request.user)
        
        # Get the specific movie
        movie = get_object_or_404(Movie, pk=pk)
        
        # Check if the movie is already in the user's watchlist
        if Watchlist.objects.filter(userProfile=user_profile, movie=movie).exists():
            messages.warning(request, f"{movie.title} is already in your watchlist.")
        else:
            # Create a new watchlist entry
            Watchlist.objects.create(userProfile=user_profile, movie=movie)
            messages.success(request, f"{movie.title} has been added to your watchlist.")
        
        # Redirect back to the movie list or another page
        return redirect('watchlist')


# View for removing a movie from the user's watchlist
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

# View for creating a new movie 
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

# View for updating a users profile
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
    
# View for updating an existing review - only if you are the user that created it
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