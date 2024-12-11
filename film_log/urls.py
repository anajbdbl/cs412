## Ana Julia Bortolossi
## anajbdbl@bu.edu
## urls for the application

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

# URL patterns for the application
urlpatterns = [
    # Home page or profiles page that shows all user profiles
    path('', views.ShowAllView.as_view(), name='profiles'),

    # A specific user's profile page identified by the primary key (pk)
    path('profile/<int:pk>', views.ProfileView.as_view(), name='profile'),

    # Page to create a new user profile
    path('create_profile/', views.CreateProfileView.as_view(), name='create_profile'),

    # URL to create a review for a movie
    path('review/create_review/', views.PostReviewView.as_view(), name='create_review'),

    # URL to update an existing review, identified by its primary key (pk)
    path('review/update/<int:pk>/', views.UpdateReviewView.as_view(), name='update_review'),

    # URL to update the user's profile (e.g., email, image)
    path('profile/update/', views.UpdateProfileView.as_view(), name='update_profile'),

    # URL that lists all movies in the database
    path('movies/', views.MovieListView.as_view(), name='all_movies'),

    # URL to view a detailed page for a specific movie, identified by its primary key (pk)
    path('movie/<int:pk>', views.MovieDetailView.as_view(), name='show_movie'),

    # URL to add a new movie to the database
    path('add_movie/', views.CreateMovieView.as_view(), name='add_movie'),

    # URL to add a friend by selecting a user profile, identified by its primary key (other_pk)
    path('profile/add_friend/<int:other_pk>/', views.CreateFriendView.as_view(), name='add_friend'),

    # URL to view suggested friends for the current user
    path('profile/friend_suggestions/', views.ShowFriendSuggestionsView.as_view(), name='friend_suggestions'),

    # URL to view the user's watchlist
    path('watchlist/', views.WatchlistView.as_view(), name='watchlist'),

    # URL to remove a movie from the user's watchlist, identified by its primary key (pk)
    path('watchlist/remove/<int:pk>/', views.RemoveFromWatchlistView.as_view(), name='remove_from_watchlist'),

    # URL to add a movie to the user's watchlist, identified by its primary key (pk)
    path('movies/<int:pk>/add_to_watchlist/', views.AddToWatchlistView.as_view(), name='add_to_watchlist'),

    # URL to delete a review by its primary key (pk)
    path('review/delete/<int:pk>/', views.DeleteReviewView.as_view(), name='delete_review'),

    # URL for login page
    path('login/', auth_views.LoginView.as_view(template_name='film_log/login.html'), name='login'),

    # URL for logout page
    path('logout/', auth_views.LogoutView.as_view(template_name='film_log/logged_out.html'), name='logout'),
]

