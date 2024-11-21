from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.ShowAllProfilesView.as_view(), name='show_all_profiles'),
    path('profile/<int:pk>', views.ProfileView.as_view(), name='show_profile'),
    path('create_profile/', views.CreateProfileView.as_view(), name='create_profile'),

    path('review/create_review/', views.PostReviewView.as_view(), name='create_review'),
    # path('profile/update/', views.UpdateProfileView.as_view(), name='update_profile'),
    # path('status/<int:pk>/update/', views.UpdateStatusMessageView.as_view(), name='update_status'),
    path('movie/<int:pk>', views.MovieDetailView.as_view(), name='show_movie'),
    path('profile/add_friend/<int:other_pk>/', views.CreateFriendView.as_view(), name='add_friend'), 
    path('profile/friend_suggestions/', views.ShowFriendSuggestionsView.as_view(), name='friend_suggestions'), 
    
    path('login/', auth_views.LoginView.as_view(template_name='mini_fb/login.html'),name='login'), 
    path('logout/', auth_views.LogoutView.as_view(template_name='mini_fb/logged_out.html'), name='logout'), 
]
