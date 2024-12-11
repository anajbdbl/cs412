## Ana Julia Bortolossi
## anajbdbl@bu.edu
## models for the application

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
# UserProfile model represents the profile of a user
class UserProfile(models.Model):
    first_name = models.CharField(max_length=30)  # First name of the user
    last_name = models.CharField(max_length=30)  # Last name of the user
    email = models.EmailField()  # Email address of the user
    profile_image_url = models.URLField(max_length=200)  # URL of the user's profile image
    birthdate = models.DateField(null=True, blank=True)  # Optional birthdate
    friends = models.ManyToManyField('self', symmetrical=True, blank=True)  # Self-referencing Many-to-Many relationship for friends
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')  # Link to the built-in User model (one-to-one)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"  # Return the full name of the user when the object is printed

    def get_reviews(self):
        # Return a queryset of the user's reviews, ordered by timestamp in descending order
        return self.reviews.all().order_by('-timestamp')

    def get_friends(self):
        # Return a list of the user's friends by checking the Friend relationship model
        friends = Friend.objects.filter(models.Q(profile1=self) | models.Q(profile2=self))
        return [friend.profile2 if friend.profile1 == self else friend.profile1 for friend in friends]
    
    def add_friend(self, other):
        # Add a friend if not already a friend (check the Friend model to prevent duplicates)
        if not Friend.objects.filter(models.Q(profile1=self, profile2=other) | models.Q(profile1=other, profile2=self)).exists():
            Friend.objects.create(profile1=self, profile2=other, timestamp=timezone.now())

    def get_friend_suggestions(self):
        # Return friend suggestions based on users who are not friends with the current user
        current_friends = set(self.get_friends())  # Get the current user's friends
        all_profiles = set(UserProfile.objects.exclude(pk=self.pk))  # Get all profiles excluding the current user
        return list(all_profiles - current_friends)  # Return users who are not current friends


# Movie model represents a movie with details like title, description, and more
class Movie(models.Model):
    title = models.CharField(max_length=255)  # Title of the movie
    description = models.TextField()  # Detailed description of the movie
    release_date = models.DateField()  # Release date of the movie
    director = models.CharField(max_length=255)  # Director of the movie
    genre = models.CharField(max_length=100)  # Genre of the movie
    poster = models.ImageField(upload_to='movie_posters/', null=True, blank=True)  # Optional movie poster image

    def __str__(self):
        return self.title  # Return the movie title when the object is printed


# Review model represents a review of a movie written by a user
class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')  # Link to the Movie being reviewed
    userProfile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='reviews')  # Link to the user's profile
    rating = models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])  # Rating given to the movie (1-5)
    review_text = models.TextField()  # Text of the review written by the user
    date_posted = models.DateTimeField(default=timezone.now)  # Date and time when the review was posted

    def __str__(self):
        return f"Review for {self.movie.title} by {self.userProfile.first_name}"  # Display review details when the object is printed


# Watchlist model represents a movie that a user has added to their watchlist
class Watchlist(models.Model):
    userProfile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='watchlist')  # Link to the user's profile
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='watchlist')  # Link to the movie in the watchlist
    date_added = models.DateTimeField(default=timezone.now)  # Date and time when the movie was added to the watchlist

    def __str__(self):
        return f"{self.userProfile.first_name}'s Watchlist: {self.movie.title}"  # Display user's watchlist entry


# Friend model represents a friendship between two users (UserProfile objects)
class Friend(models.Model):
    profile1 = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='friend_set1')  # One user in the friendship
    profile2 = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='friend_set2')  # The other user in the friendship
    timestamp = models.DateTimeField(default=timezone.now)  # Date and time when the friendship was established

    def __str__(self):
        return f"{self.profile1} & {self.profile2}"  # Display friendship details
