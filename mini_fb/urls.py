from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.ShowAllProfilesView.as_view(), name='show_all_profiles'),
    path('profile/<int:pk>', views.ShowProfilePageView.as_view(), name='show_profile'),
    path('create_profile/', views.CreateProfileView.as_view(), name='create_profile'),
    path('status/create_status/', views.CreateStatusMessageView.as_view(), name='create_status'),
    path('profile/update/', views.UpdateProfileView.as_view(), name='update_profile'),
    path('status/<int:pk>/update/', views.UpdateStatusMessageView.as_view(), name='update_status'),
    path('status/<int:pk>/delete/', views.DeleteStatusMessageView.as_view(), name='delete_status'),
    path('image/<int:pk>/delete/', views.DeleteImageView.as_view(), name='delete_image'), ## Assignment 7
    path('profile/add_friend/<int:other_pk>/', views.CreateFriendView.as_view(), name='add_friend'), ## Assignment 8
    path('profile/friend_suggestions/', views.ShowFriendSuggestionsView.as_view(), name='friend_suggestions'), ## Assignment 8
    path('profile/news_feed/', views.ShowNewsFeedView.as_view(), name='news_feed'), ## Assignment 8
    path('login/', auth_views.LoginView.as_view(template_name='mini_fb/login.html'),name='login'), ## Assignment 9
    path('logout/', auth_views.LogoutView.as_view(template_name='mini_fb/logged_out.html'), name='logout'), ## Assignment 9
]
