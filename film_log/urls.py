from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.ShowAllView.as_view(), name='profiles'),
    path('profile/<int:pk>', views.ProfileView.as_view(), name='profile'),
    path('create_profile/', views.CreateProfileView.as_view(), name='create_profile'),

    path('review/create_review/', views.PostReviewView.as_view(), name='create_review'),
    path('review/update/<int:pk>/', views.UpdateReviewView.as_view(), name='update_review'),
    path('profile/update/', views.UpdateProfileView.as_view(), name='update_profile'),
    path('movies/', views.MovieListView.as_view(), name='all_movies'),
    path('movie/<int:pk>', views.MovieDetailView.as_view(), name='show_movie'),
    path('add_movie/', views.CreateMovieView.as_view(), name='add_movie'),
    path('profile/add_friend/<int:other_pk>/', views.CreateFriendView.as_view(), name='add_friend'), 
    path('profile/friend_suggestions/', views.ShowFriendSuggestionsView.as_view(), name='friend_suggestions'), 
    path('watchlist/', views.WatchlistView.as_view(), name='watchlist'),
    path('watchlist/remove/<int:pk>/', views.RemoveFromWatchlistView.as_view(), name='remove_from_watchlist'),

    path('login/', auth_views.LoginView.as_view(template_name='film_log/login.html'),name='login'), 
    path('logout/', auth_views.LogoutView.as_view(template_name='film_log/logged_out.html'), name='logout'), 
]
